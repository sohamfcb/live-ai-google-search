# 🛠️ **Real-Time AI Search Hub**  

A Streamlit-powered application that combines **Google Programmable Search Engine** and **Groq LLM** to deliver real-time, contextual, and insightful answers based on live search results and prior conversation history.  

---

## 🚀 **Overview**  

This application acts as a smart assistant capable of **browsing the internet** to fetch information and deliver well-structured summaries. Powered by:  
1. **Google Programmable Search API** for retrieving live search results.  
2. **Groq LLM** (using LLaMA-3.1) for generating insightful and context-aware responses.  
3. **Streamlit** for an interactive user interface.  

---

## ✨ **Features**  

- **Real-Time Internet Search**: Queries the web using Google Programmable Search Engine.  
- **Context-Aware Responses**: Maintains a conversation history to ensure continuity in responses.  
- **Structured Summaries**: Provides clear answers with sections like Key Insights, Examples, and Conclusion.  
- **Interactive Interface**: User-friendly input and output via Streamlit.  
- **Error Handling**: Industry-standard practices for robust performance.  

---

## 🛠️ **Tech Stack**  

- **Frontend**: Streamlit  
- **Backend**: LangChain (for conversational agent and memory)  
- **Language Model**: Groq's LLaMA-3.1  
- **Search API**: Google Custom Search API  
- **Environment Management**: Python, dotenv  

---

## 📦 **Installation**  

Follow these steps to set up the project locally:  

### 1. Clone the Repository  

```bash
git clone https://github.com/yourusername/realtime-ai-search-hub.git
cd realtime-ai-search-hub
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file in the project root with the following content:

```bash
GOOGLE_CSE_ID = your_google_cse_id
GOOGLE_SEARCH_API_KEY = your_google_api_key
GROQ_API_KEY = your_groq_api_key
```

Replace the placeholders with your API keys.

### 5. Run the Application

```bash
streamlit run app.py
```

## **Usage**

1. Enter your query in the input field.
2. Click Send to retrieve live search results.
3. The AI will process search results and return:

   - Key Insights
   - Detailed Explanation
   - Examples (if available)
   - Conclusion

The application maintains prior context for follow-up questions.
