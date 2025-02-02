import streamlit as st
import boto3
from sqlalchemy import create_engine
from langchain_community.chat_models import BedrockChat
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from urllib.parse import quote_plus
from botocore.config import Config
import pandas as pd
st.title("Valorant Players Query Assistant on 2022 Dataset")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Valorant Players Query Assistant. How can I help you?"}]

# Create a sidebar
with st.sidebar:
    st.text("Hey there!")
    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Valorant Players Query Assistant. How can I help you?"}]
        st.rerun()

# AWS Configuration
connathena = ""
portathena = ''
schemaathena = ''
s3stagingathena = quote_plus('s3://')
wkgrpathena = 'primary'
aws_access_key_id = ''
aws_secret_access_key = ''

if aws_access_key_id and aws_secret_access_key and connathena:
    try:
        session = boto3.Session(
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        bedrock_config = Config(
            region_name='',
            signature_version='v4',
            retries={
                'max_attempts':9 ,
                'mode': 'standard'
            }
        )
        
        bedrock_client = session.client(
            service_name='bedrock-runtime',
            config=bedrock_config,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        connection_string = (
            f"awsathena+rest://@{connathena}:{portathena}/"
            f"{schemaathena}?"
            f"s3_staging_dir={s3stagingathena}&"
            f"work_group={wkgrpathena}&"
            f"region_name=us-east-1"
        )

        engine_athena = create_engine(connection_string, 
                                    connect_args={'session': session})

        llm = BedrockChat(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            client=bedrock_client,
            model_kwargs={
                "max_tokens": 1024,
                "temperature": 0.0
            }
        )

        QUERY = """
You are a SQL assistant. Your task is to generate SQL queries based on user input for a database named 'valorant'. 
Ensure that the SQL query is syntactically valid and formatted for execution in AWS Athena.

Tables and Columns in database
    Table Name: 
        player_details 
    Schema and Columns description:
        `player_idid`: 'This is the primary key to find the player. It is the Id to find a player',
        `player_handle`: 'player handle referes to the in game name of the player',
        `player_first_name`: 'refers to the players first name',
        `player_last_name`: 'refers to the players last name',
        `player_status`: 'refers to the players status',
        `player_home_team_id`: 'refers to the team id of the player. Can be used to find the team name. It also serves as a foreign key to connect with team_details table.'
    Table Name: 
        leagues
    Schema and Columns description: 
        `league_id`: 'Id for the league. It is the primary key',
        `league_region`: 'Region where the league hosted',
        `league_name`: 'Name of the league',
        `league_slug`: 'Slug name of the league'
    Table Name: 
        tour_details
    Schema and Columns description: 
        `tour_id`: 'Contains the Id for the tournament. Also a primary key for this table, that could help in finding the tournament name',
        `tour_status`: 'Describes the status of the tournament, whether or not published',
        `tour_league_id`: 'contains the league id for the given tournament. can serve as foreign key to find the league name to connect with leagues table',
        `tour_name`: 'Name of the tournament'
    Table Name: 
        mapping_details
    Schema and Columns description: 
        `platformgameid`: 'Refers to the Id of the platform',
        `matchid`: 'Refers to the Match Id',
        `esportsgameid`: 'Refers to the matchid in esports',
        `tournamentid`: 'Refers to the Id of the Tournament, can also be ',
        `teammapping`: 'Contains Ids of the teams for the given match, can be served as foreign key, to find the names of teams in team_details table. ',
        `participantmapping`: 'Contains Ids of the players for the given match, can be served as foreign key, to find the names of players.'
    Table Name: 
        team_details
    Schema and Columns descritpion: 
        `team_id`: 'Identifies the details of the team. Also the primary key in this table',
        `team_acronym`: 'Contains the team acronym',
        `team_home_league_id`: 'Contains the league id, can be served as foreign key, to find the league name in leagues table',
        `team_slug`: 'Contains the slug name of the team',
        `team_name`: 'Contains the name of the team'        


Rules:
- Do not include plain English in the SQL query.
- Only include valid SQL syntax supported by Athena.
- Validate user input to avoid incorrect SQL generation.
- Join schemas as needed using the format:
  SELECT * FROM valorant.leagues l
  JOIN valorant.tour_details t
  ON l.league_id = t.tour_league_id
- If would like to join tables team_details and player_details 
    SELECt * from valorant.player_details pd
    join valorant.team_details td 
    ON pd.home_team_id = td.team_id
- If you would like to join tour_details with mappings use tournamentid of mapping_details to join with tour_id from tour_details table
- If you would like to join mapping_details with player_details use participantmapping of mapping_details to join with players_idid from player_details using "like" instead of "=" because
participantmapping is a huge string contains a lot of playerids 

Question: {question}
"""


        db = SQLDatabase(engine_athena)
        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

        # Display chat history
        def is_question(text):
            question_words = ['what', 'how', 'when', 'where', 'who', 'which', 'why', 'can', 'show',"could"]
            return any(word in text.lower() for word in question_words)
        
        # Display chat history
        st.header("Chat History")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        user_question = st.chat_input("Ask your question about Valorant players:")

        if user_question:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_question)
            
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        if is_question(user_question):
                            # Generate SQL query and fetch data
                            question = QUERY.format(question=user_question)
                            raw_query_result = db_chain.run(question)
                            
                            # Generate natural language explanation from query results
                            explanation_prompt = f"""
                            Based on the query results below, provide a clear and concise explanation in natural language:
                            {raw_query_result}
                            
                            Please format the response in only user-friendly way and include relevant details from the query results. But nothing about query
                            """
                            
                            explanation_message = llm.invoke(explanation_prompt)
                            explanation_content = explanation_message.content if hasattr(explanation_message, 'content') else str(explanation_message)
                            
                            # Display the response
                            st.write(explanation_content)
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": explanation_content})
                        else:
                            # Handle conversational input gracefully
                            conversational_prompt = f"""
                    The user said: "{user_question}". Respond in a friendly and engaging way as an assistant.
                    """
                    
                            conversational_response = llm.invoke(conversational_prompt)
                            conversational_content = conversational_response.content if hasattr(conversational_response, 'content') else str(conversational_response)
                            
                            # Display dynamic conversational response
                            st.write(conversational_content)
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": conversational_content})
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
else:
    st.info("Please check AWS credentials and connection details")