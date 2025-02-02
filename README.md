# 🔥 Valorant Player Insights Chatbot  
![valorant_architecture](https://github.com/user-attachments/assets/a0f73baf-bbfa-46b9-aa1e-bfec76e65cd8)

This project is a **Streamlit-powered web application** that enables users to ask questions about **Valorant players**, with responses generated using **AWS Athena, BedrockChat, and LangChain**. The chatbot dynamically constructs and executes SQL queries against a **Valorant database**, returning both raw results and **human-friendly explanations**.  

---

## 🚀 Key Components & Workflow  

### 🖥️ 1. User Interface & Session Management  

#### 🎭 **Streamlit Chat Interface**  

#### 🔄 **Session Management**  


---

### ☁️ 2. AWS & Database Configuration  

#### 🔑 **AWS Integration**  
✅ **Amazon Athena** – for querying structured Valorant data.  
✅ **AWS Bedrock** – for generating responses using an **LLM (Large Language Model)**.  

#### 📊 **Athena SQL Connection**  
A **SQLAlchemy-powered connection** is established to Athena, using:  
- An **S3 staging directory** for query execution.  
- Workgroup and schema configurations to optimize performance.  
Allows the chatbot to **fetch player statistics, match details, and other Valorant-related data**.  

---

### 🤖 3. Language Model & Query Generation  

#### 🧠 **LLM Setup with BedrockChat**  
The chatbot utilizes **Amazon Bedrock’s LLM** via **LangChain**.

#### 📝 **SQL Query Construction**  
The chatbot dynamically builds **SQL queries** using a structured template that includes:  
📌 **Predefined table schema** (e.g., `player_details`, `leagues`, `tour_details`, etc.).  
📌 **Defined rules for table joins**, ensuring accurate results.  
📌 **User’s query injected** into the SQL template for precise execution.  

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

---

🔥 **Ask, Explore, and Dominate the Game with Data!** 🎮  

---
