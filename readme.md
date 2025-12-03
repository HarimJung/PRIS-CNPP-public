
# ⚛️ PRIS-CIP Integrated Analytical Platform 

This project is a **Streamlit-based web application** that provides comprehensive insights into specific national nuclear programs by combining data from the **IAEA's Power Reactor Information System (PRIS)** and country-specific **Nuclear Power Policy Documents (CNPP)**, along with real-time Q&A capabilities.

---

## 🌟 Key Features 

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

# ⚛️ PRIS-CIP Analytical Platform



**PRIS-CIP Analytical Platform**은 Streamlit을 기반으로 구축된 **RAG(Retrieval-Augmented Generation)** 시스템입니다. IAEA PRIS(Power Reactor Information System)의 통계 데이터와 CNPP(Country Nuclear Power Profiles)의 정책 문서를 통합하여, 국가별 핵발전 프로그램에 대한 심층 분석 리포트와 실시간 Q&A 챗봇 기능을 제공합니다.

---

## 🏗️ System Architecture


# ⚛️ PRIS-CIP Analytical Platform

The **PRIS-CIP Analytical Platform** is a **RAG (Retrieval-Augmented Generation)** system built on Streamlit. By integrating statistical data from the IAEA PRIS (Power Reactor Information System) and policy documents from CNPP (Country Nuclear Power Profiles), it provides in-depth analysis reports and real-time Q&A chatbot capabilities regarding national nuclear power programs.

---

## 🏗️ System Architecture

This project utilizes **Streamlit** as the frontend/backend host and implements a retrieval-augmented generation pipeline using **LangChain** and **FAISS**.

### 🎥 System Demo
[![PRIS-CIP Demo Video](https://img.youtube.com/vi/EnGxLJSyZ6Q/hqdefault.jpg)](https://youtu.be/EnGxLJSyZ6Q)

```mermaid
graph TD
    %% 1. Define Nodes (Main)
    A["User/Client<br>(Streamlit App)"]
    B["Streamlit Server<br>(Frontend)"]
    H["Tableau Public Server"]

    %% 2. Define Subgraph (Backend)
    subgraph Backend ["Backend Logic (Python)"]
        direction TB
        C{"DataAnalyzer:<br>PRIS.csv Read"}
        D["FAISS Vector Store:<br>faiss_index"]
        E["OpenAI Embeddings Model"]
        F["ChatOpenAI LLM:<br>GPT-4"]
        G["LangChain RAG Chain:<br>Prompt/Parser"]
    end

    %% 3. Data and Request Flow
    A -- "1. Interaction (Filter/Question)" --> B
    B -- "2. Call Methods" --> C
    
    %% Static Data Flow
    C -- "3. Statistical Summary" --> G
    
    %% RAG Flow: Guided Analysis & Q&A
    B -- "4. Question/Topics" --> G
    G -- "5. Text Embedding" --> E
    E -- "6. Vector Search Query" --> D
    D -- "7. Relevant Context" --> G
    G -- "8. LLM Prompt & Synthesis" --> F
    F -- "9. Final Report/Answer" --> B
    B -- "10. Display Result" --> A

    %% External Integration
    B -- "11. Embed Tableau URL" --> H
    H -- "12. Display Interactive Viz" --> A
    
    %% 4. Styling
    classDef external fill:#f9f,stroke:#333;
    class H external
