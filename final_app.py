import os
import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple, Set
import streamlit.components.v1 as components
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# OpenAI API Key
os.environ["OPENAI_API_KEY"] = ""


# Constants
COUNTRIES = ['Korea, Republic of', 'United States of America', 'China', 'Japan', 'United Arab Emirates', 'Canada', 'Egypt']
REACTOR_TYPES = ['PWR', 'BWR', 'PHWR', 'VVER', 'EPR']


# Dynamic Analysis Questions by Country (Maintaining original structure)
DYNAMIC_QUESTIONS = {
   "Korea, Republic of": {
       "Nuclear Policy Framework 📋": [
           "How does Korea's nuclear energy policy align with its carbon neutrality goals?",
           "What is Korea's position on nuclear plant life extension and new builds?",
           "How does Korea integrate nuclear with renewable energy sources?"
       ],
       "Technology Leadership 🔬": [
           "What are the key features and deployment status of the APR-1400?",
           "How is Korea advancing its SMR development through SMART reactor?",
           "What is Korea's nuclear technology export strategy and achievements?"
       ],
       "Safety & Regulation 🛡️": [
           "How does KINS implement its regulatory oversight functions?",
           "What are the key safety features in Korean nuclear designs?",
           "How does Korea manage its nuclear emergency preparedness system?"
       ],
       "Fuel Cycle Management ⚛️": [
           "What is Korea's spent fuel management policy and infrastructure?",
           "How does Korea ensure nuclear fuel supply security?",
           "What R&D is being conducted for advanced fuel technologies?"
       ]
   },
   "United Arab Emirates": {
       "Barakah Project 🏗️": [
           "What is the current status of the Barakah Nuclear Power Plant?",
           "How is the APR-1400 technology being implemented in UAE?",
           "What are the key milestones in the Barakah construction timeline?"
       ],
       "Regulatory Framework 📊": [
           "How does FANR regulate nuclear activities in UAE?",
           "What safety standards are implemented at Barakah?",
           "How is nuclear emergency preparedness managed?"
       ],
       "Capacity Building 👥": [
           "How is UAE developing its nuclear workforce?",
           "What international partnerships support UAE's nuclear program?",
           "What is the role of ENEC in program implementation?"
       ]
   },
   "Egypt": {
       "El Dabaa Project 🏭": [
           "What is the scope and timeline of the El Dabaa NPP project?",
           "How is Egypt cooperating with Russia on the VVER technology?",
           "What are the key project milestones and challenges?"
       ],
       "Nuclear Infrastructure 🔧": [
           "How is Egypt establishing its nuclear regulatory framework?",
           "What measures are in place for nuclear safety and security?",
           "How is Egypt developing its nuclear workforce?"
       ],
       "Energy Planning ⚡": [
           "How does nuclear fit into Egypt's energy strategy?",
           "What are the economic and environmental benefits expected?",
           "How will El Dabaa impact regional energy security?"
       ]
   },
   "China": {
       "Expansion Program 📈": [
           "What is China's nuclear capacity target for 2025/2030?",
           "How many units are currently under construction?",
           "What new sites are being developed for nuclear power?"
       ],
       "Technology Development 🔬": [
           "What is the status of Hualong One deployment?",
           "How is China developing its SMR technology?",
           "What advanced reactor designs is China pursuing?"
       ],
       "Industrial Capability 🏭": [
           "How has China localized nuclear technology?",
           "What is China's nuclear export strategy?",
           "How is China's nuclear supply chain organized?"
       ]
   },
   "United States of America": {
       "Fleet Management 🏢": [
           "What is the status of nuclear plant life extensions?",
           "How is the existing fleet's performance being optimized?",
           "What regulatory changes support continued operation?"
       ],
       "Advanced Reactors 🔬": [
           "What is the progress on SMR deployment?",
           "How does NRC regulate new reactor technologies?",
           "What advanced reactor designs are being developed?"
       ],
       "Policy Support 📜": [
           "How do federal policies support nuclear energy?",
           "What incentives exist for new nuclear projects?",
           "How is nuclear waste management being addressed?"
       ]
   },
   "Japan": {
       "Restart Program 🔄": [
           "What is the status of nuclear plant restarts?",
           "How have safety requirements been enhanced post-Fukushima?",
           "What is the timeline for remaining restart reviews?"
       ],
       "Safety Enhancement 🛡️": [
           "What new safety measures have been implemented?",
           "How has the regulatory framework been strengthened?",
           "What emergency preparedness improvements were made?"
       ],
       "Energy Policy ⚡": [
           "What is nuclear's role in Japan's energy mix?",
           "How does nuclear support decarbonization goals?",
           "What is the policy on plant life extension?"
       ]
   },
   "Canada": {
       "CANDU Technology 🔬": [
           "How is the CANDU fleet being maintained and upgraded?",
           "What life extension programs are in progress?",
           "How is CANDU technology being exported?"
       ],
       "SMR Leadership 🚀": [
           "What is Canada's SMR deployment roadmap?",
           "How is regulatory framework adapting for SMRs?",
           "What SMR designs are being developed?"
       ],
       "Nuclear Innovation 💡": [
           "What R&D programs are prioritized?",
           "How is nuclear supporting clean energy goals?",
           "What new applications are being explored?"
       ]
   }
}


class DataAnalyzer:
   """Data Analysis Engine"""
  
   def __init__(self):
       self.df = pd.read_csv("PRIS.csv")
  
   def get_country_summary(self, country: str) -> str:
       """Generate statistical summary for selected country"""
       country_data = self.df[self.df['Country'] == country]
       operational = country_data[country_data['Status'] == 'Operational']
      
       # Filter out empty dates and get the most recent connection
       valid_dates = country_data['First Grid Connection'].dropna()
       latest_connection = "No connected units" if len(valid_dates) == 0 else max(valid_dates)
      
       summary = f"""Nuclear Power Statistics for {country}:
       - Total Units: {len(country_data)}
       - Operational Units: {len(operational)}
       - Total Capacity: {operational['Gross Electrical Capacity [MW]'].sum():,.0f} MW
       - Reactor Types: {', '.join(country_data['Type'].unique())}
       - Latest Connection: {latest_connection}
       """
       return summary


class RAGQueryEngine:
   """RAG Search and Response Generation Engine"""
  
   def __init__(self):
       self.embeddings = OpenAIEmbeddings()
       try:
           self.vectorstore = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
       except Exception as e:
           st.error(f"Failed to load FAISS index: {str(e)}")
           self.vectorstore = None
       self.llm = ChatOpenAI(model="gpt-4", temperature=0)
      
       # Initialize prompt template for guided analysis (maintaining original)
       self.analysis_prompt = ChatPromptTemplate.from_template("""
       [SYSTEM ROLE]
       You are an expert nuclear policy analyst providing comprehensive analysis of nuclear power programs.
       Synthesize the provided information into a professional analytical report.


       [ANALYSIS CONTEXT]
       Selected Analysis Topics:
       {questions}


       Statistical Context:
       {data_summary}


       Reference Documents:
       {context}


       [VISUALIZATION CONTEXT]
       The user is viewing a Tableau dashboard showing:
       - Nuclear capacity trends
       - Reactor type distribution
       - Operational performance metrics


       [OUTPUT INSTRUCTIONS]
       Generate a comprehensive analytical report that:
       1. Addresses each selected topic with evidence-based analysis
       2. Integrates statistical insights from the data summary
       3. References relevant policy documents and regulations
       4. Provides strategic implications and future outlook
       5. Uses clear headings and professional tone


       Format the response in markdown with appropriate sections and bullet points.
       """)
      
       # Initialize prompt template for ad-hoc questions (maintaining original)
       self.qa_prompt = ChatPromptTemplate.from_template("""
       [SYSTEM ROLE]
       You are a nuclear industry expert providing accurate, data-driven answers.


       [CONTEXT]
       User Question: {question}


       Statistical Context:
       {data_summary}


       Reference Information:
       {context}


       [TASK]
       Provide a clear, concise answer that:
       1. Directly addresses the question
       2. Cites specific data points and sources
       3. Maintains professional tone
       4. Indicates if information is limited or uncertain
       """)
  
   def get_relevant_documents(self, query: str, country: str) -> List[str]:
       """Search for relevant documents with country filter"""
       if self.vectorstore is None:
           return ["Error: FAISS index could not be loaded."]
      
       try:
           docs = self.vectorstore.similarity_search(
               query,
               k=5,
               filter={"country": country} if country else None
           )
          
           formatted_docs = []
           for doc in docs:
               source = f"[{doc.metadata['source']}]"
               if doc.metadata['source'] == 'CNPP':
                   source += f" {doc.metadata['country']} Policy Document"
               formatted_docs.append(f"{source}: {doc.page_content}")
          
           return formatted_docs
          
       except Exception as e:
           st.error(f"Error during document search: {str(e)}")
           return [f"Error: Failed to search documents: {str(e)}"]
  
   def generate_analysis(self, questions: List[str], country: str, data_summary: str) -> str:
       """Generate comprehensive analysis report"""
       relevant_docs = []
       for question in questions:
           relevant_docs.extend(self.get_relevant_documents(question, country))
      
       rag_chain = (
           {
               "questions": lambda x: "\n".join(x["questions"]),
               "context": lambda x: "\n\n".join(set(relevant_docs)),  # Remove duplicates
               "data_summary": lambda x: x["data_summary"]
           }
           | self.analysis_prompt
           | self.llm
           | StrOutputParser()
       )
      
       return rag_chain.invoke({
           "questions": questions,
           "data_summary": data_summary
       })
  
   def answer_question(self, question: str, country: str, data_summary: str) -> str:
       """Generate answer for ad-hoc question"""
       relevant_docs = self.get_relevant_documents(question, country)
      
       qa_chain = (
           {
               "question": lambda x: x["question"],
               "context": lambda x: "\n\n".join(relevant_docs),
               "data_summary": lambda x: x["data_summary"]
           }
           | self.qa_prompt
           | self.llm
           | StrOutputParser()
       )
      
       return qa_chain.invoke({
           "question": question,
           "data_summary": data_summary
       })


def main():
   # Enhanced Page Configuration
   st.set_page_config(
       page_title="PRIS-CIP Analytical Platform",
       page_icon="⚛️",
       layout="wide",
       initial_sidebar_state="expanded"
   )


   # Global Custom CSS (header bar, tabs, containers, shadows)
   st.markdown("""
   <style>
   /* Header bar */
   .app-header {
       background: linear-gradient(90deg,#0d47a1,#1976d2);
       color: white;
       padding: 18px 24px;
       border-radius: 8px;
       margin-bottom: 18px;
   }
   .app-header h1 { margin:0; font-size:28px; }


    /* Topic cards and report container */
   .topic-card {
       background: #ffffff;
       border: 1px solid #e6eef8;
       border-radius: 10px;
       padding: 14px;
       box-shadow: 0 6px 18px rgba(13,71,161,0.08);
       margin-bottom: 12px;
   }
   .topic-card h4 { margin-top:0; color:#0d47a1; }

   /* Hide JSON display */
   .stJson {
       display: none !important;
   }

   /* Execute button area with full width */
   .execute-area { 
       margin: 24px 0;
       padding: 0 24px;
       width: 100% !important;
   }
   
   .execute-area .stButton {
       width: 100% !important;
   }
   
   .execute-area .stButton > button {
       width: 100% !important;
       padding: 0.75rem 2rem !important;
       font-size: 1.1rem;
       text-align: left;
   }

   /* Report container */
   .report-container {
       background: #f8f9fa;
       border: 1px solid #e9ecef;
       border-radius: 10px;
       padding: 24px;
       box-shadow: 0 6px 18px rgba(33,150,243,0.06);
       margin: 24px 0;
       width: 100% !important;
       max-width: none !important;
   }


   /* Tableau placeholder sizing */
   .tableau-placeholder { border-radius:10px; overflow:hidden; }


   /* Tabs styling hint (best-effort, Streamlit uses dynamic classes) */
   .stTabs [role="tab"]:focus { outline: none; }
   </style>
   """, unsafe_allow_html=True)


   # Initialize session state
   if 'selected_questions' not in st.session_state:
       st.session_state.selected_questions = set()
   if 'chat_history' not in st.session_state:
       st.session_state.chat_history = []


   # Main Header (styled bar)
   st.markdown('<div class="app-header"><h1>⚛️ PRIS-CIP Analytical Platform</h1></div>', unsafe_allow_html=True)


   # Sidebar (all filters must be here)
   with st.sidebar:
       st.markdown("# � Data Filters")
       selected_country = st.selectbox("Select Country", COUNTRIES)
       selected_types = st.multiselect("Select Reactor Types", REACTOR_TYPES)


       viz_filter_state = {"country": selected_country, "reactor_types": selected_types}
       st.markdown("---")
       st.markdown("**Active Filters**")
       st.json(viz_filter_state)


   # Main Content Tabs
   tab1, tab2 = st.tabs(["📊 Integrated Analysis & Tableau", "💬 Real-Time Q&A Chatbot"])


   # Initialize analyzers (preserve logic)
   data_analyzer = DataAnalyzer()
   rag_engine = RAGQueryEngine()


   with tab1:
       # Tableau Dashboard (large)
       st.markdown('<h2 style="color:#0d47a1;">📈 Interactive PRIS Data Dashboard</h2>', unsafe_allow_html=True)
       # Country name mapping for Tableau
       country_mapping = {
           "Korea, Republic of": "Korea",
           "United States of America": "United States of America",
           "China": "China",
           "Japan": "Japan",
           "United Arab Emirates": "United Arab Emirates",
           "Canada": "Canada",
           "Egypt": "Egypt"
       }

       # Construct Tableau Public URL with parameters
       base_url = "https://public.tableau.com/views/PRISOverview_AI/PRIS"
       tableau_params = {
           ":language": "en-US",
           ":display_count": "n",
           ":origin": "viz_share_link",
           ":showVizHome": "n",
           ":embed": "y",
           "Country": country_mapping[selected_country].replace(" ", "%20"),  # Map country name and URL encode spaces
           "Type": ",".join(selected_types).replace(" ", "%20") if selected_types else "All"
       }
       
       # Create parameter string
       param_str = "&".join([f"{k}={v}" for k, v in tableau_params.items()])
       tableau_embed_url = f"{base_url}?{param_str}"
       
       # Embed Tableau dashboard with dynamic filters
       components.html(
           f"""
           <div class='tableauPlaceholder' style='width: 100%; height: 750px;'>
               <iframe src='{tableau_embed_url}'
                       frameborder='0' 
                       style='width: 100%; height: 100%;'
                       allowfullscreen>
               </iframe>
           </div>
           """,
           height=750
       )


       # Guided Analysis Grid (2x2 or 2x3 depending on topics)
       st.markdown('<h2 style="color:#0d47a1;">🎯 Guided Analysis Topics</h2>', unsafe_allow_html=True)


       if selected_country in DYNAMIC_QUESTIONS:
           topics = list(DYNAMIC_QUESTIONS[selected_country].items())
           num_topics = len(topics)
           # Use 2 columns for up to 4 topics (2x2), else 3 columns
           num_cols = 2 if num_topics <= 4 else 3
           rows = (num_topics + num_cols - 1) // num_cols


           idx = 0
           for r in range(rows):
               cols = st.columns(num_cols)
               for c in range(num_cols):
                   if idx >= num_topics:
                       break
                   topic, questions = topics[idx]
                   with cols[c]:
                       # Each topic enclosed in styled container
                       with st.container():
                           st.markdown(f'<div class="topic-card"><h4>{topic}</h4>', unsafe_allow_html=True)
                           for q in questions:
                               if st.checkbox(q, key=f"{selected_country}_{q}"):
                                   st.session_state.selected_questions.add(q)
                               elif q in st.session_state.selected_questions:
                                   st.session_state.selected_questions.remove(q)
                           st.markdown('</div>', unsafe_allow_html=True)
                   idx += 1


       # Enforce selection limit and show warning
       if len(st.session_state.selected_questions) > 3:
           st.warning("⚠️ Maximum 3 questions can be selected at once!")
           st.session_state.selected_questions = set(list(st.session_state.selected_questions)[:3])


       # Full width Execute Button
       st.markdown('<div class="execute-area">', unsafe_allow_html=True)
       if st.button("🔍 Execute Integrated Analysis", use_container_width=True):
               if not st.session_state.selected_questions:
                   st.info("Select up to 3 guided questions to run the analysis.")
               else:
                   with st.spinner("🔄 Generating comprehensive analysis..."):
                       data_summary = data_analyzer.get_country_summary(selected_country)
                       analysis = rag_engine.generate_analysis(
                           list(st.session_state.selected_questions),
                           selected_country,
                           data_summary
                       )
                       # Display report in distinct container
                       st.markdown('<div class="report-container">', unsafe_allow_html=True)
                       st.markdown('## 📑 Comprehensive Analytical Report')
                       st.markdown(analysis)
                       
                       # Add source citations
                       st.markdown('---')
                       st.markdown("""
                       <div style='font-size: 0.8em; color: #666; margin-top: 20px;'>
                       **Sources:**
                       - Statistical data from PRIS Database
                       - Policy documents from Country Nuclear Power Profiles (CNPP)
                       - Analysis generated using retrieved context from the knowledge base
                       </div>
                       """, unsafe_allow_html=True)
                       st.markdown('</div>', unsafe_allow_html=True)
       st.markdown('</div>', unsafe_allow_html=True)


   with tab2:
       st.markdown('<h2 style="color:#0d47a1;">💡 Real-Time Q&A Chatbot</h2>', unsafe_allow_html=True)
       # Render chat history
       for msg in st.session_state.chat_history:
           if msg.get('role') == 'user':
               with st.chat_message('user'):
                   st.markdown(msg.get('content'))
           else:
               with st.chat_message('assistant'):
                   st.markdown(msg.get('content'))


       # Chat input
       user_question = st.chat_input("Ask a question about nuclear power programs...")
       if user_question:
           # Append user message
           st.session_state.chat_history.append({'role': 'user', 'content': user_question})
           with st.chat_message('user'):
               st.markdown(user_question)


           with st.chat_message('assistant'):
               with st.spinner('� Searching knowledge base...'):
                   data_summary = data_analyzer.get_country_summary(selected_country)
                   answer = rag_engine.answer_question(user_question, selected_country, data_summary)
                   st.session_state.chat_history.append({'role': 'assistant', 'content': answer})
                   st.markdown(answer)


if __name__ == "__main__":
   main()

