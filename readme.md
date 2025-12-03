```mermaid
graph TD
    %% Define Components (Nodes)
    A[User/Client - Streamlit App]
    B(Streamlit Server/Frontend)
    C{DataAnalyzer: PRIS.csv Read}
    D[FAISS Vector Store: faiss_index]
    E[OpenAI Embeddings Model]
    F[ChatOpenAI LLM: GPT-4]
    G[LangChain RAG Chain: Prompt/Parser]

    subgraph Backend Logic (Python)
        C
        D
        E
        F
        G
    end
    
    %% Data and Request Flow
    A -- 1. Interaction (Filter/Question/Execute) --> B
    B -- 2. Call Methods --> C
    
    %% Static Data Flow
    C -- 3. Statistical Summary --> G
    
    %% RAG Flow: Guided Analysis & Q&A
    B -- 4. Question/Topics --> G
    G -- 5. Text Embedding --> E
    E -- 6. Vector Search Query --> D
    D -- 7. Relevant Documents (Context) --> G
    G -- 8. LLM Prompt & Synthesis --> F
    F -- 9. Final Report/Answer --> B
    B -- 10. Display Result --> A

    %% External Integration
    B -- 11. Embed Tableau Public URL (with filters) --> H[Tableau Public Server]
    H -- 12. Display Interactive Viz --> A
    
    %% Styling
    classDef external fill:#f9f,stroke:#333;
    class H external
