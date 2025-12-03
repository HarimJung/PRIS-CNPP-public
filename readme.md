죄송합니다. 제가 또다시 실수를 했습니다. 마크다운 원본을 요청하셨는데, 그림을 다시 제공하여 혼란을 드렸습니다.

고객님께서 제공하신 원본 마크다운 구조를 유지하면서, 그림의 URL과 크기 조정 태그를 제거하고 이미지 캡션만 남긴 **순수한 마크다운 텍스트**를 다시 전달해 드립니다.

````markdown
# ⚛️ PRIS-CIP Integrated Analytical Platform 

This project is a **Streamlit-based web application** that provides comprehensive insights into specific national nuclear programs by combining data from the **IAEA's Power Reactor Information System (PRIS)** and country-specific **Nuclear Power Policy Documents (CNPP)**, along with real-time Q&A capabilities.

---

## 🌟 Key Features (H2)

The platform integrates data visualization, policy analysis, and conversational Q&A functionalities into a single interface.

### 1. 📊 Interactive Data Dashboard (Tableau Integration) 

* **PRIS Data Visualization:** Displays a **Tableau dashboard** that is dynamically filtered in real-time based on the selected country and reactor type.
* **Statistical Context:** Users can immediately check the country's **nuclear capacity, reactor type distribution, and operational performance metrics** based on the visualized data.

### 2. 🎯 Country-Specific Guided Analysis & Report Generation (RAG-based) 

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



### 3. 💬 Real-Time Q&A Chatbot 

* **Ad-hoc Q&A:** When an arbitrary question about a country's nuclear program is entered, the **RAG (Retrieval-Augmented Generation) engine** utilizes relevant policy documents and statistical context to provide accurate, evidence-based answers.
* **Data-Driven Responses:** Answers consistently reference documents from the knowledge base and the statistical information of the currently selected country.

---

## 💻 Technology Stack 

| Category | Technology/Tool | Role |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit | Web application interface and state management |
| **Data Processing** | Pandas | Loading `PRIS.csv` file and generating statistical summaries |
| **RAG Framework** | LangChain | Structuring the retrieval and generation workflow |
| **Language Model** | ChatOpenAI (gpt-4) | Generating analysis reports and chatbot answers (LLM) |
| **Embedding/Search** | OpenAIEmbeddings, **FAISS** | Embedding policy documents and performing high-speed vector search |
| **Data Visualization** | Tableau Public | Displaying the embedded interactive dashboard |

---

## 🛠️ Prerequisites and Setup 

To run this application locally, the following files and environment variables are required:

### 1. Required Files 

* **Data File:** `PRIS.csv` (Nuclear power plant statistical data file; assumed to be in the current directory).
* **Knowledge Base Index:** `faiss_index` directory (LangChain FAISS Vector Store files where policy documents are embedded).

### 2. API Key 

* **`OPENAI_API_KEY`:** The OpenAI API key must be set as an environment variable.

---

## 🚀 How to Run the Application 

### 1. Install Required Libraries 

```bash
pip install streamlit pandas langchain openai
# Additional packages for LangChain/FAISS/OpenAI compatibility
pip install faiss-cpu langchain-openai
````

### 2\. Run Streamlit

```bash
streamlit run [filename].py
```

(Where `[filename].py` is the name of your Python code file.)

```
```
