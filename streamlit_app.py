import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def main():
    #st.set_page_config(page_title="My Streamlit App")

    # Define your menu options here
    menu = ["Home", "Page 1", "Page 2"]

    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Home":
        home()
    elif choice == "Page 1":
        page1()
    elif choice == "Page 2":
        page2()

def home():
    st.title("Welcome to my app!")
    st.write("Please select a page from the menu.")

    # Define the questions
    questions = [
        'What is your name?',
        'How old are you?',
        'Where are you from?',
        'What is your favorite color?'
    ]

    # Initialize the answers
    answers = {}

    # Loop through the questions and get user input
    for question in questions:
        answer = st.text_input(question)
        answers[question] = answer

def page1():
    st.title("Page 1")
    st.write("This is the first page of my app.")

    rows = run_query("SELECT TOP 5 * FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.REGION;")

    # Display the results in a Streamlit table
    st.table(rows)

def page2():
    st.title("Page 2")
    st.write("This is the second page of my app.")

if __name__ == "__main__":
    main()


