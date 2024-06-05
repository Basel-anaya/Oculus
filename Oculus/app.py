# Import the necessary Python packages.
import os
import time
from datetime import date
import csv

# Import the necessary packages from langchain
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

# streamlit
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

# amadeus tools
from amadeus_tools import AmadeusFlightOffersSearchTool

# Import the necessary packages from Pydantic to be able to use structured tools.
from pydantic.v1 import BaseModel, BaseSettings, Field
import asyncio
import nest_asyncio
# nest_asyncio.apply()

# Import the necessary packages from Pydantic to be able to use structured tools.
from pydantic.v1 import BaseModel, BaseSettings, Field
import asyncio
import nest_asyncio
# nest_asyncio.apply()

# Create a new event loop and set it as the current event loop in the current OS thread
asyncio.set_event_loop(asyncio.new_event_loop())

# Now you can apply nest_asyncio to the new event loop
nest_asyncio.apply()



## fetching year, month and day from current system date for llm system context
today = date.today()
current_year = today.year
current_month=today.month
current_date= today.day
# print("current year","\t","current month","\t","current date\n")
# print(current_year,"\t",current_month,"\t",current_date)

# system message
system_message = SystemMessage(content="""
You are a helpful, respectful and honest travel agent.
Your main objective is to have a conversation with a human and help them make interesting travel and vacation plans, based on their needs, wants, desires, especially taking into account any limiting factors such as disabilities or age.
You should help them define the objective of their travel and then lookup the options for them in your tools.
You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses.
The main objective is devided into several tasks which are as follow:
  -Focus on the human's intent for their travel or vacation, Analyze it and Provide a relevant, structured response that helps them to define what they want to do.
  -Think about the potential options they have for their travel such as: the amount of time they have available, flight times and price ranges, hotel star ratings, sightseeing options.
  -To be able to help, you can ask the human to provide any specific flight ideas they have, but you should also suggest potential novel options to them.
  -The necessary flight details you need from the human to look up flights are stated in the tool description.
  -After you receive enough information from the human, You can use one of the available tools to help you with the task, ONLY IF IT IS NECESSARY.
Additional Guidelines for Enhanced User Experience:
- Indirect references to time of travel: If human mentions a time reference during conversation, like 'this year', 'current year', 'this month', 'current month', then equate that to the {0}, {0},{1} and {1} respectively.
- No mention of year explicitly: If human mentions no year in the travel date, then consider that to be current year {0}. Confirm with human if they meant the month to be {1} and then act accordingly
- No mention of month explicitly: If human mentions no month in the travel date, then consider that to be current month {1}. Confirm with human if they meant the month to be {1} and then act accordingly
The tools Should NOT be used unless its Absolutely necessary.
The available tools you have access to, are as follow:
  -Amadeus flight offers search: This tool can be used to make a get request to the Amadeus api and retrieve any flights details related to the Human's questions.
Overall, You are a powerful system that can help with asking for Humans details in a conversation, And use it to create an interesting and unique vacation plan tailored to their requirements.
Finally remember, Your main objective is to have a conversation, Do not provide the same response twice.
""")
contentParam=system_message.content.format(current_year, current_month)
system_message=SystemMessage(content=contentParam)


# open ai LLM
llm = ChatOpenAI(temperature=0,model = 'gpt-3.5-turbo-16k')

# setup tools and agent
flight_offers_search_tool = AmadeusFlightOffersSearchTool()
tools = [flight_offers_search_tool]

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=25, return_messages=True)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=True,
    early_stopping_method="generate",
    memory=memory,
    agent_kwargs={"system_message": system_message},
    agent=AgentType.OPENAI_FUNCTIONS)


# streamlit
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

st_callback = StreamlitCallbackHandler(st.container())


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message on first load
if not st.session_state.messages:
    welcome_message = "👋 Hi! Welcome to the Oculus Travel Assistant, how can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    st_callback = StreamlitCallbackHandler(st.container())
    assistant_response = agent.run(prompt, callbacks=[st_callback])

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split(' '):
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})



# test prompt;
# hey can you search a flight between london and madrid for me this october 23rd?