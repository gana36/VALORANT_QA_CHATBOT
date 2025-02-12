# 🔥 Valorant Player Insights Chatbot  
![valorant_architecture](https://github.com/user-attachments/assets/000a7187-3e2a-4637-98fa-5b1006b08b6c)

Project demo can be found <a href="https://github.com/gana36/VALORANT_QA_CHATBOT/blob/main/demo_QA.gif>here</a>
This project is a **Streamlit-powered web application** that enables users to ask questions about **Valorant players**, with responses generated using **AWS Athena, BedrockChat, and LangChain**. The chatbot dynamically constructs and executes SQL queries against a **Valorant database**, returning both raw results and **human-friendly explanations**.  

---

## 🚀 Key Components & Workflow  

### 🖥️ 1. User Interface & Session Management  

#### 🎭 **Streamlit Chat Interface**  
Streamlit is a framework, we used it as a tool for the end user(non-technical) to interact with database stored in AWS S3. 

#### 🔄 **Session Management**  
For enhancing usability, chatbot stores chat history in the session state. Also a button to clear the whole chat is provided to reset the conversation instantly.

---

### ☁️ 2. AWS & Database Configuration  

#### 🔑 **AWS Integration**  
✅ **Amazon Athena** – for querying structured Valorant data in S3.  
✅ **AWS Bedrock** – for generating responses [SQL query and plain text from tabular format] using an **LLM (Large Language Model)**.  

#### 📊 **Athena SQL Connection**  
A **SQLAlchemy-powered connection** is established to Athena, using:  
- An **S3 staging directory** for query execution.  
 
Allows the chatbot to **fetch player statistics, match details, and other Valorant-related data**.  

---

### 🤖 3. Language Model & Query Generation  

#### 🧠 **LLM Setup with BedrockChat**  
The chatbot utilizes **Anthropic Claude** via **LangChain**.

#### 📝 **SQL Query Construction**  
The chatbot dynamically builds **SQL queries** using a structured template that includes:  
📌 **Predefined table schema** (e.g., `player_details`, `leagues`, `tour_details`, etc.).  
📌 **Defined rules for table joins**, ensuring accurate results.  
  

---

### 🔍 4. Processing User Input  

#### 🧐 **Question Detection**  
Before processing a query, the chatbot checks if the input contains **keywords like "what," "how," or "when"**, ensuring that the request is SQL-related.  

#### 🏆 **SQL Execution Path**  
If the query requires data retrieval:  
🔹 The chatbot **formats the SQL query** with the user’s input.  
🔹 **LangChain’s SQLDatabaseChain** generates and validates the Athena-compatible SQL query.  
🔹 The query is executed, and raw results are retrieved.  

#### 🗣️ **Natural Language Explanation**  
Instead of showing raw SQL results, the chatbot asks the LLM to generate a **clear, easy-to-understand explanation** – avoiding any reference to SQL syntax. This makes insights **accessible to all users**, even those unfamiliar with databases.  

#### 💬 **Conversational Mode**  
If the input isn’t SQL-related, the chatbot switches to a **free-flow conversation mode**.
