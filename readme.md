
# ⚛️ PRIS-CIP Integrated Analytical Platform (H1)

This project is a **Streamlit-based web application** that provides comprehensive insights into specific national nuclear programs by combining data from the **IAEA's Power Reactor Information System (PRIS)** and country-specific **Nuclear Power Policy Documents (CNPP)**, along with real-time Q&A capabilities.

---

## 🌟 Key Features (H2)

The platform integrates data visualization, policy analysis, and conversational Q&A functionalities into a single interface.

### 1. 📊 Interactive Data Dashboard (Tableau Integration) (H3)

* **PRIS Data Visualization:** Displays a **Tableau dashboard** that is dynamically filtered in real-time based on the selected country and reactor type.
* **Statistical Context:** Users can immediately check the country's **nuclear capacity, reactor type distribution, and operational performance metrics** based on the visualized data.

### 2. 🎯 Country-Specific Guided Analysis & Report Generation (RAG-based) (H3)

* **Dynamic Analysis Topics:** Provides a detailed list of analysis questions specific to the selected country (e.g., Korea, UAE, China) covering:
    * Policy
    * Technological leadership
    * Safety and regulation
    * Fuel cycle management
* **Comprehensive Analysis Report Generation Process:** When the user selects and executes 3 questions, the application performs the following steps:
    1.  It searches the knowledge base (**FAISS Index**) for policy documents related to the selected questions.
    2.  It integrates the retrieved policy context with the **PRIS statistical summary data**.
    3.  It generates a professional **Comprehensive Analysis Report** using the **GPT-4 model**. 

[Image of a diagram illustrating the RAG process of retrieval, integration, and generation]


### 3. 💬 Real-Time Q&A Chatbot (H3)

* **Ad-hoc Q&A:** When an arbitrary question about a country's nuclear program is entered, the **RAG (Retrieval-Augmented Generation) engine** utilizes relevant policy documents and statistical context to provide accurate, evidence-based answers.
* **Data-Driven Responses:** Answers consistently reference documents from the knowledge base and the statistical information of the currently selected country.

---

## 💻 Technology Stack (H2)

| Category | Technology/Tool | Role |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit | Web application interface and state management |
| **Data Processing** | Pandas | Loading `PRIS.csv` file and generating statistical summaries |
| **RAG Framework** | LangChain | Structuring the retrieval and generation workflow |
| **Language Model** | ChatOpenAI (gpt-4) | Generating analysis reports and chatbot answers (LLM) |
| **Embedding/Search** | OpenAIEmbeddings, **FAISS** | Embedding policy documents and performing high-speed vector search |
| **Data Visualization** | Tableau Public | Displaying the embedded interactive dashboard |

---

## 🛠️ Prerequisites and Setup (H2)

To run this application locally, the following files and environment variables are required:

### 1. Required Files (H3)

* **Data File:** `PRIS.csv` (Nuclear power plant statistical data file; assumed to be in the current directory).
* **Knowledge Base Index:** `faiss_index` directory (LangChain FAISS Vector Store files where policy documents are embedded).

### 2. API Key (H3)

* **`OPENAI_API_KEY`:** The OpenAI API key must be set as an environment variable.

---

## 🚀 How to Run the Application (H2)

### 1. Install Required Libraries (H3)

```bash
pip install streamlit pandas langchain openai
# Additional packages for LangChain/FAISS/OpenAI compatibility
pip install faiss-cpu langchain-openai
````

### 2\. Run Streamlit (H3)

```bash
streamlit run [filename].py
```

(Where `[filename].py` is the name of your Python code file.)

```
```
