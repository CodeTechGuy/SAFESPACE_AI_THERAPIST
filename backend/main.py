# # Step1: Setup FastAPI backend
# from fastapi import FastAPI
# from pydantic import BaseModel
# import uvicorn

# from ai_agent import graph, SYSTEM_PROMPT, parse_response

# app = FastAPI()

# # Step2: Receive and validate request from Frontend
# class Query(BaseModel):
#     message: str



# @app.post("/ask")
# async def ask(query: Query):
#     inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
#     #inputs = {"messages": [("user", query.message)]}
#     stream = graph.stream(inputs, stream_mode="updates")
#     final_response = parse_response(stream)

#     # Step3: Send response to the frontend
#     return {"response": final_response}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    



# Step1: Setup FastAPI backend
import re

from fastapi import FastAPI , Form
from pydantic import BaseModel
import uvicorn

from ai_agent import agent, SYSTEM_PROMPT, parse_response

app = FastAPI()

# Step2: Request schema
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    inputs = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query.message}
        ]
    }

    # ✅ Invoke agent (NEW WAY)
    response = agent.invoke(inputs)

    # ✅ Parse response (updated version)
    tool_called_name, final_response = parse_response(response)

    # Step3: Send response to frontend
    return {
        "response": final_response,
        "tool_called": tool_called_name
    }


from fastapi.responses import PlainTextResponse
from xml.etree.ElementTree import Element , tostring
from xml.sax.saxutils import escape

def create_twilio_response(message: str) -> PlainTextResponse:
    """
    Create an XML response for Twilio's WhatsApp API.
    <Response>
    <Message>Your message here</Message>
    </Response>
    """

    root = Element("Response")
    message_element = Element("Message")

    safe_message = escape(message)  # Ensure message is XML-safe

    message_element.text = safe_message
    root.append(message_element)
    xml_response = tostring(root, encoding="utf-8", method="xml")
    return PlainTextResponse(content=xml_response, media_type="application/xml")


def trim_response(text: str, limit: int = 1200) -> str:
    if len(text) <= limit:
        return text
    
    # Cut at last full stop before limit
    trimmed = text[:limit]
    last_dot = trimmed.rfind(".")
    
    if last_dot != -1:
        return trimmed[:last_dot + 1]

    return trimmed + "..."
    # return text[:limit] + "..."

def clean_formatting(text: str) -> str:
    # remove markdown tables
    text = re.sub(r"\|.*?\|", "", text)

    # remove markdown symbols
    text = re.sub(r"[#*_`]", "", text)

    return text.strip()



def format_for_whatsapp(text: str) -> str:
    lines = text.split(". ")
    return "\n\n".join(lines)


@app.post("/whatsapp_ask")
async def whatsapp_ask(Body: str = Form(...)):
    user_text = Body.strip() if Body else ""
    inputs = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }

    response = agent.invoke(inputs)
    tool_called_name, final_response = parse_response(response)

    # FIX: ensure it's always a string
    if not final_response:
        final_response = "I'm here to support you. Sorry, I couldn't process your request at the moment."


    if not isinstance(final_response, str):
        final_response = str(final_response)

    # final_response = parse_response(response)
    final_response = clean_formatting(final_response)
    final_response = format_for_whatsapp(final_response)
    final_response = trim_response(final_response)


    print("WHATSAPP RESPONSE LENGTH:", len(final_response))
    print("WHATSAPP RESPONSE:", final_response)



    return create_twilio_response(final_response)
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5729, reload=True)

    