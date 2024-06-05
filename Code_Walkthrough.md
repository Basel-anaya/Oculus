### How the streamlit code functionality works.

- Step One: Import all the neccesary packages, tools codes each from different script file in the same directory, and define environment variables.

- Step Two: Create a vector storage to store the conversation as embeddings on each interaction between the user and the chatbot.

  Vector store uses openAi api to transform the conversation to embeddings, and pass it to an index to arrange the embeddings in specific order based on faiss ('Facebook AI Similarity Search') package, and a document storage object that's needed for langchain agent, then its all passed to a retriever object that can handle inserting and retrieving the embeddings back and forth between the llm and the vector store.

 ![vector store](https://github.com/fellowship/travel-agent-lam/assets/114405334/29047d3c-d4d4-4fe5-a05f-9b4566e5496c)
 
- Step Three: The system prompt that controls the chatbot behaviour, This step is the most important and complicated part in all the code, 1 wrong word can change the chatbot behaviour totally, And i am honestly sorry i haven't had enough time to work on it beside writing all the codes and testing them and debugging all the errors that comes from the tools.

![system prompt](https://github.com/fellowship/travel-agent-lam/assets/114405334/53c82b94-335c-4e00-90a6-21e13db3306f)

- Step Four: define a function to load a csv file ('if exists') that contain the previous conversation, and save it in an object as a list of messages.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/dc886724-b1ce-4b6b-8617-71c59daf5782)

- Step Five: Initialize the tools and pass them to a list. and later pass this list to the agent.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/8aeeedb5-2a4c-41ff-9e4b-4a13a85095e8)

- Step Six: pass the list of messages obtained from step 4 to streamlit chat history then initialize the loading function from step 4, also create 2 different types of memory objects, a conversation memory that can handle a natural language conversation and also inject streamlit chat history inside it, a vectory memory that can uses the vector storage that we defined in step 2, then we pass both memories to a combined memory wrapper and later pass the wrapper object to the agent.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/61a7cc90-2335-438c-af37-61d78abb1540)

 - Step Seven: Initialize openAi agent with gpt3.5 turpo as an llm, the list of tools we defined earlier, the combined memory wrapper, the system prompt we defined earlier and finally a special type of memory that is made specificaly for function calling agent, as you realize we are using 4 different memory types at the moment.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/6f107755-fc9c-42e8-b6b7-870190f9aefc)

 - Step Eight: Initialize streamlit callback handler, to handle all the writing interactions between the agent and streamlit interface, Define a function to initialize chat history for streamlit interface, then define a function to load the chathistory saved on the csv file to streamlit insterface.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/ce18a9d7-45f6-45aa-b4cb-ab30f90fd962)

 - Step Nine: Define a function to save chat history from streamlit interface to a csv file, with 2 columns, 1st column is the role (User, Assistant)

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/6eb75757-ba6c-47b3-98a9-0d84954ebd7e)

 - Step Ten: Define an if statement to check if there are no previous messages then it displays a welcome message to the user, Also define a for loop to display the chat history for each message's role on streamlit interface.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/16b7121b-4ccf-41a2-bd8d-0213c5839563)

 Final step: Define an if statement to Display the user message on the interface then use the agent run method with the user message and recieve the agent response then display the agent response on the interface and finally initialize the save chat history function that we defined earlier, to save the chat history after each conversation turn.

![image](https://github.com/fellowship/travel-agent-lam/assets/114405334/ffd01729-1c07-4cb8-9835-00e496c411a5)
