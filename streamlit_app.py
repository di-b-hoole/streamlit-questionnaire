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

#@st.cache_data(ttl=600)
def run_query(query,expectResult=1):
    with conn.cursor() as cur:
        cur.execute(query)
        if expectResult != 0:
            return cur.fetchall()


def main():

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
    if st.button('Submit data'):
            run_query(query,0)
    

def Answers():
    st.title("Answers")
    st.write("This is the first page of my app.")

    if st.button('Refresh data'):
        rows = run_query("SELECT * FROM ANSWERS;")

        # Display the results in a Streamlit table
        st.table(rows)

    

def page2():
    st.title("Page 2")
    st.write("This is the second page of my app.")

    with st.form("my_form"):
        st.write("Inside the form")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

        st.write("Outside the form")

if __name__ == "__main__":
    main()


