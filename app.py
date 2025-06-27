import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure API key

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


# Function to load model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# Define your prompt
prompt = [ 
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION.

    Example 1:
    Question: How many entries of records are present?
    SQL: SELECT COUNT(*) FROM STUDENT;

    Example 2:
    Question: Tell me all the students studying in maths class.
    SQL: SELECT * FROM STUDENT WHERE CLASS = "maths";

    Convert the following question to an SQL command (no ``` or the word SQL in the output):
    """
]

# Set page config
st.set_page_config("SmartQuery: AI-Powered Student DB Tool")

# Dark navy-blue theme with white text
st.markdown("""
    <style>
        body, .main {
            background-color: #0E1117;  /* Dark navy-blue */
            color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4, h5, h6, .stHeader {
            color: #FFFFFF;
        }

        .stTextInput > label {
            font-size: 18px;
            color: #CCCCCC;
            font-weight: 600;
        }

        .stTextInput input {
            background-color: #1C1F2E;
            color: white;
            border: 1px solid #444;
            padding: 10px;
            border-radius: 6px;
        }

        .stButton > button {
            background-color: #1E2A78;  /* Deep blue */
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            border: none;
        }

        .stButton > button:hover {
            background-color: #2639B5;
            color: #FFFFFF;
        }

        .sql-result {
            background-color: #1A1E30;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 12px;
            font-size: 24px;
            font-weight: 600;
            color: #FFFFFF;  /* White output */
            box-shadow: 0px 0px 12px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)


# Title
st.header("📊 SmartQuery: AI-Powered Student DB Tool")

# Input box
question = st.text_input("Input:", key="input")
submit = st.button("Ask the Question")

# On click
if submit:
    response = get_gemini_response(question, prompt)
    response = read_sql_query(response, "student.db")
    st.subheader("The response is:")
    for row in response:
        print(row)
        st.markdown(f"<div class='sql-result'>{', '.join(map(str, row))}</div>", unsafe_allow_html=True)
