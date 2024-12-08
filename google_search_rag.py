from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

import os
import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Set Streamlit page configuration
st.set_page_config(page_title="Real-Time AI Search Hub")
st.title("Live AI Insights via Google Search")

# Custom Google Search Class
class GoogleSearch:
    def __init__(self, api_key, cse_id):
        """
        Initializes the Google Custom Search API service.
        Args:
            api_key (str): Google API key.
            cse_id (str): Google Custom Search Engine ID.
        """
        try:
            self.service = build("customsearch", "v1", developerKey=api_key)
            self.cse_id = cse_id
        except Exception as e:
            st.error("Error initializing Google Search API.")
            st.stop()  # Stop Streamlit execution
            raise e

    def search(self, query):
        """
        Performs a Google search and formats the results into a structured prompt.
        Args:
            query (str): User query for the search.
        Returns:
            str: A formatted prompt containing the search results.
        """
        try:
            # Template for structured results prompt
            custom_prompt = """
                I have the following search results related to "{query}". Please analyze these results and provide a comprehensive, well-structured summary. Include the most relevant insights, comparisons (if applicable), and any notable trends or points. Format the summary as follows:

                1. **Key Insights**: Provide the most important takeaways from the search results.
                2. **Detailed Explanation**: Expand on the context and details provided in the results, offering a deeper understanding of the topic.
                3. **Examples or Case Studies** (if applicable): Include any examples or case studies mentioned in the results that illustrate the key points.
                4. **Conclusion**: Summarize the overall implications or significance of the findings.

                Here are the search results:
                {search_results}

                Make sure to provide a clear and concise answer with structured sections for easy reading.
            """

            # Execute search
            response = self.service.cse().list(q=query, cx=self.cse_id).execute()
            search_results = response.get('items', [])
            
            # Format search results
            formatted_results = ""
            for item in search_results:
                title = item.get('title', 'No Title')
                snippet = item.get('snippet', 'No Snippet')
                link = item.get('link', 'No Link')
                formatted_results += f"**Title**: {title}\n**Snippet**: {snippet}\n**Link**: {link}\n\n"

            # Return the final prompt
            return custom_prompt.format(query=query, search_results=formatted_results)

        except Exception as e:
            st.error("Error retrieving search results.")
            raise e

# Load environment variables
try:
    load_dotenv()
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not all([google_cse_id, google_search_api_key, groq_api_key]):
        st.error("Missing required environment variables.")
        st.stop()
except Exception as e:
    st.error("Failed to load environment variables.")
    st.stop()
    raise e

# Initialize Google Search engine
try:
    engine = GoogleSearch(api_key=google_search_api_key, cse_id=google_cse_id)
except Exception as e:
    st.error("Error initializing Google Search engine.")
    raise e

# Define Google Search tool for the agent
search_tool = Tool(
    name="Google Search",
    description="Retrieve information from Google Programmable Search Engine.",
    func=engine.search
)

# Initialize Groq LLM
try:
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
except Exception as e:
    st.error("Failed to initialize Groq LLM.")
    st.stop()
    raise e

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define Conversation Memory for the agent
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# Define Prompt Template
prompt_template = """
You are an assistant capable of browsing the internet and answering questions based on search results. You will remember prior conversations and take them into account for a more accurate response. Return your answers in markdown format.

Here is the context of the conversation:
{chat_history}

Now, answer the following question based on your previous conversation and the current query:
{query}
"""

# Prompt template using messages
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_template),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}")
    ]
)

# Initialize the agent (ensure it’s done only once)
if "agent" not in st.session_state:
    try:
        st.session_state.agent = initialize_agent(
            tools=[search_tool],
            llm=llm,
            agent="chat-conversational-react-description",
            memory=memory,
            handle_parsing_errors=True
        )
    except Exception as e:
        st.error("Error initializing the agent.")
        st.stop()
        raise e

# User input for query
user_input = st.text_input("Message Llama:")
btn = st.button("Send")

if btn:
    if user_input:
        try:
            st.text("Browsing the Internet...")

            # Format the query with context
            formatted_prompt = prompt_template.format(
                chat_history="\n".join([msg.content for msg in st.session_state.chat_history]),
                query=user_input
            )

            # Invoke the agent to get the response
            response = st.session_state.agent.invoke({
                'input': formatted_prompt,
                'chat_history': st.session_state.chat_history
            })

            # Display the response
            st.markdown(response['output'])

            # Append messages to chat history
            st.session_state.chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=response['output'])
            ])

        except Exception as e:
            st.error("An error occurred while processing your request.")
            raise e
    else:
        st.warning("Please enter your question.")
