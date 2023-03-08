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
    menu = ["Home", "Answers", "Page 2"]

    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Home":
        home()
    elif choice == "Answers":
        Answers()
    elif choice == "Page 2":
        page2()

def home():
    st.title("Welcome to my app!")
    st.write("Please select a page from the menu.")

    options = ["Dog", "Cat", "Bird", "Fish", "Reptile"]
    selected_option = st.selectbox("Select an option", options)

    # Define the SQL query and parameters
    query = f"INSERT INTO ANSWERS (Question, answer) VALUES ('What is your favourite animal','{selected_option}')"

    # Execute the query
    run_query(query)
    conn.commit()


def Answers():
    st.title("Answers")
    st.write("This is the first page of my app.")

    rows = run_query("SELECT * FROM ANSWERS;")

    # Display the results in a Streamlit table
    st.table(rows)

def page2():
    st.title("Page 2")
    st.write("This is the second page of my app.")

if __name__ == "__main__":
    main()


