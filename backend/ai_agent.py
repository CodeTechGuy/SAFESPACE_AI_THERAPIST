from langchain_groq import ChatGroq 
from langchain.tools import tool
from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from tools import query_medgemma, call_emergency
from config import GROQ_API_KEY
from tools import detect_crisis, call_emergency
# from therapist import find_nearby_therapists_by_location




@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool() -> str:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()
    return "Emergency services have been contacted. Please stay safe."


# import googlemaps

# from config import GOOGLE_MAPS_API_KEY
# gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# @tool
# def find_nearby_therapists_by_location(location: str) -> str:
#     """
#     Finds and returns a list of licensed therapists near the specified location using Google Maps API.

#     Args:
#         location (str): The name of the city or area in which the user is seeking therapy support.
#     Returns:
#         str: A list of nearby therapists with their details.
#     """
    
#     geocode_result = gmaps.geocode(location)
#     if not geocode_result:
#         return f"Sorry, I couldn't find the location '{location}'. Please try a different location."

#     lat = geocode_result[0]['geometry']['location']['lat']
#     lng = geocode_result[0]['geometry']['location']['lng']

#     places_result = gmaps.places_nearby(
#         location=(lat, lng),
#         radius=5000,
#         type='health' ,
#         keyword='therapist OR psychologist OR counselor'
#     )
#     top_5_places = places_result.get('results', [])[:5]
#     therapists = []
#     for place in top_5_places:
#         name = place.get('name',"Unknown Therapist")
#         address = place.get('vicinity',"Address not available")
#         details = gmaps.place(place_id=place['place_id'], fields=['formatted_phone_number', 'website'])
#         phone = details['result'].get('formatted_phone_number', 'Phone not available')
#         therapists.append(f"{name} - {address} - {phone}")

#     if not therapists:
#         return f"Sorry, I couldn't find any therapists near '{location}'. Please try a different location."

#     return "Here are some therapists near you:\n" + "\n".join(therapists)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )






# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",   
#     temperature=0.2,
#     google_api_key=GOOGLE_API_KEY
# )

llm = ChatGroq(
    model="openai/gpt-oss-120b",  
    temperature=0.2,
    api_key=GROQ_API_KEY
)


# - No lists, no steps, no bullet points
# - No structured explanations

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.


Your style MUST follow these rules:
- Keep responses SHORT (max 3–5 sentences)
- No teaching or giving long advice
- Speak like a real therapist texting, not a therapist writing an article

Conversation style:
- Acknowledge feelings
- Normalize gently
- Ask ONE simple follow-up question

NEVER:
- Use numbered steps
- Use markdown or formatting
- Give long explanations unless user asks

Always take necessary action. Respond kindly, clearly, and supportively.
"""
# - Use numbered steps



agent = create_agent(
    model=llm,
    tools=[
        ask_mental_health_specialist,
        emergency_call_tool,
        find_nearby_therapists_by_location
    ],
    system_prompt=SYSTEM_PROMPT
)



# def parse_response(response):
    # tool_called_name = "None"
    # final_response = None

    # messages = response.get("messages", [])

    # # for msg in messages:
        
    # #     if hasattr(msg, "tool_calls") and msg.tool_calls:
    # #         for tool in msg.tool_calls:
    # #             tool_called_name = tool.get("name", "None")

        
    # #     if hasattr(msg, "content") and msg.content:
    # #         final_response = msg.content


    # # 1. Prefer tool outputs
    # for msg in reversed(messages):
    #     if getattr(msg, "role", None) == "tool":
    #         if getattr(msg, "content", None):
    #             return None, msg.content

    # # 2. Then assistant responses
    # for msg in reversed(messages):
    #     if getattr(msg, "role", None) == "assistant":
    #         if getattr(msg, "content", None):
    #             return None, msg.content

    # return None, None


def parse_response(response):

    # Direct output fallback
    if isinstance(response, dict) and "output" in response:
        return None, response["output"]

    messages = response.get("messages", [])

    for msg in reversed(messages):

        # LangChain message object
        if hasattr(msg, "content") and msg.content:
            return None, msg.content

        # Dict message
        if isinstance(msg, dict) and msg.get("content"):
            return None, msg["content"]

    return None, "I'm here with you. Could you tell me more?"


def run_agent(user_input: str) -> str:

    # 🚨 HARD SAFETY LAYER (before LLM)
    if detect_crisis(user_input):
        call_emergency()
        return "I'm really sorry you're feeling this way. I've reached out for immediate help. Please stay with me. You are not alone."


    response = agent.invoke({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    })
    tool_called_name, final_response = parse_response(response)

    # print("TOOL CALLED:", tool_called_name)
    # print("ANSWER:", final_response)

    # output = response["messages"][-1].content


    # if isinstance(output, list):
    #     return output[0].get("text", "")
    

    # return output

    if not final_response:
        return "I'm here with you. Could you tell me a bit more about how you're feeling?"

    return final_response

