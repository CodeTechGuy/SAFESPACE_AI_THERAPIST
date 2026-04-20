# from langchain.agents import tool
# from tools import query_medgemma, call_emergency

# @tool
# def ask_mental_health_specialist(query: str) -> str:
#     """
#     Generate a therapeutic response using the MedGemma model.
#     Use this for all general user queries, mental health questions, emotional concerns,
#     or to offer empathetic, evidence-based guidance in a conversational tone.
#     """
#     return query_medgemma(query)


# @tool
# def emergency_call_tool() -> None:
#     """
#     Place an emergency call to the safety helpline's phone number via Twilio.
#     Use this only if the user expresses suicidal ideation, intent to self-harm,
#     or describes a mental health emergency requiring immediate help.
#     """
#     call_emergency()


# @tool
# def find_nearby_therapists_by_location(location: str) -> str:
#     """
#     Finds and returns a list of licensed therapists near the specified location.

#     Args:
#         location (str): The name of the city or area in which the user is seeking therapy support.

#     Returns:
#         str: A newline-separated string containing therapist names and contact info.
#     """
#     return (
#         f"Here are some therapists near {location}, {location}:\n"
#         "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
#         "- Dr. James Patel - +1 (555) 987-6543\n"
#         "- MindCare Counseling Center - +1 (555) 222-3333"
#     )


# # Step1: Create an AI Agent & Link to backend
# from langchain_openai import ChatOpenAI
# from langchain.agents import create_agent
# from config import OPENAI_API_KEY


# tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
# llm = ChatOpenAI(model="gemini-2.5-flash", temperature=0.2, api_key=OPENAI_API_KEY)

# SYSTEM_PROMPT = """ 
# You are an AI engine supporting mental health conversations with warmth and vigilance.
# You have access to three tools:

# 1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
# 2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
# 3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

# Always take necessary action. Respond kindly, clearly, and supportively.
# """

# graph = create_agent( model=llm, tools=tools , system_prompt=SYSTEM_PROMPT, agent_type="zero-shot-react-description")

# def parse_response(stream):
#     tool_called_name = "None"
#     final_response = None

#     for s in stream:
#         # Check if a tool was called
#         tool_data = s.get('tools')
#         if tool_data:
#             tool_messages = tool_data.get('messages')
#             if tool_messages and isinstance(tool_messages, list):
#                 for msg in tool_messages:
#                     tool_called_name = getattr(msg, 'name', 'None')

#         # Check if agent returned a message
#         agent_data = s.get('agent')
#         if agent_data:
#             messages = agent_data.get('messages')
#             if messages and isinstance(messages, list):
#                 for msg in messages:
#                     if msg.content:
#                         final_response = msg.content

#     # return tool_called_name, final_response
#     return final_response


# """if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED: ", tool_called_name)
#         print("ANSWER: ", final_response)"""
        












from langchain_groq import ChatGroq 
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import query_medgemma, call_emergency
from config import GOOGLE_API_KEY , GROQ_API_KEY


# -------------------- TOOLS --------------------

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
    # return "Emergency services have been contacted. Please stay safe."


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
        f"Here are some therapists near {location}:\n"
        "- Search on Practo or Google Maps\n"
        "- Look for licensed psychologists nearby\n"
        "- Consider online therapy platforms"
    )


# -------------------- LLM (Gemini FIXED) --------------------

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",   # ✅ FIXED MODEL
#     temperature=0.2,
#     google_api_key=GOOGLE_API_KEY
# )

llm = ChatGroq(
    model="openai/gpt-oss-120b",   # ✅ FIXED MODEL
    temperature=0.2,
    api_key=GROQ_API_KEY
)
# -------------------- SYSTEM PROMPT --------------------

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""


# -------------------- AGENT --------------------

agent = create_agent(
    model=llm,
    tools=[
        ask_mental_health_specialist,
        emergency_call_tool,
        find_nearby_therapists_by_location
    ],
    system_prompt=SYSTEM_PROMPT
)


# -------------------- SIMPLE INVOKE FUNCTION --------------------
def parse_response(response):
    tool_called_name = "None"
    final_response = None

    messages = response.get("messages", [])

    for msg in messages:
        # Check tool calls
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool in msg.tool_calls:
                tool_called_name = tool.get("name", "None")

        # Get final response
        if hasattr(msg, "content") and msg.content:
            final_response = msg.content

    return tool_called_name, final_response



def run_agent(user_input: str) -> str:
    response = agent.invoke({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    })
    tool_called_name, final_response = parse_response(response)

    print("TOOL CALLED:", tool_called_name)
    print("ANSWER:", final_response)

    output = response["messages"][-1].content

    # ✅ Fix structured output
    if isinstance(output, list):
        return output[0].get("text", "")
    

    

    return output


"""response = agent.invoke({
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
})

tool_called_name, final_response = parse_response(response)

print("TOOL CALLED:", tool_called_name)
print("ANSWER:", final_response)"""