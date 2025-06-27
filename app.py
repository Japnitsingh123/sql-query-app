import streamlit as st
import os
import sqlite3
import google.generativeai as genai

##configure  API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


##function to load model
 
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([prompt[0],question])
    return response.text

##function to retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

##define your prompt
prompt =[ 
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

##streamlit setup
st.set_page_config("I can retrieve any sql query")
st.header("app to retrieve data from database")
question=st.text_input("Input:",key="input")
submit=st.button("ask the question")

#if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    response=read_sql_query(response,"student.db")
    st.subheader("the response is")
    for row in response:
        print(row)
        st.header(row) 

    