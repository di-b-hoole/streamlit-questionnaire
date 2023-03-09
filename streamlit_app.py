import streamlit as st
import snowflake.connector

import pandas as pd

st.set_page_config(
    page_title="Chat GPT - Power Hour",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://power-hour-questionnaire.streamlit.app/',
        'Report a bug': "https://power-hour-questionnaire.streamlit.app/",
        'About': "Chat GPT - Power Hour"
    }
)

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
    st.title("Power Hour 3023-03-08")
    
    menu = ["Favourite Pet", "Questions", "Answers"]

    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Favourite Pet":
        Fav_Pet()
    elif choice == "Questions":
        Questions()
    elif choice == "Answers":
        Answers()

def Fav_Pet():
    st.title("Choose your favourite pet")

    pets = ["Dog", "Cat", "Bird", "Fish", "Reptile"]
    favourite_pet = st.selectbox("Select you favourite pet:", pets)

    # Define the SQL query and parameters
    query = f"INSERT INTO FAV_PET (PET) VALUES ('{favourite_pet}');"

    # Execute the query
    if st.button('Submit data'):
        run_query(query,0)
        st.write(favourite_pet)

def Questions():
    st.title("Please answer the below questions :)")

    genders = ['Male', 'Female', 'Rather not say']

    with st.form("my_form"):
        name_val = st.text_input("Name:")
        age_val = st.slider('How old are you?', 20, 100, 25)
        Dog_val = st.number_input('How many Dogs do you have', min_value=0, max_value=100, value=0, step=1)
        Cat_val = st.number_input('How many Cats do you have', min_value=0, max_value=100, value=0, step=1)
        Bird_val = st.number_input('How many Birds do you have', min_value=0, max_value=100, value=0, step=1)
        Fish_val = st.number_input('How many Fish do you have', min_value=0, max_value=100, value=0, step=1)
        Reptile_val = st.number_input('How many Reptiles do you have', min_value=0, max_value=100, value=0, step=1)
        gender_val = st.selectbox('Gender:',genders)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            query = f"INSERT INTO ANSWERS (NAME,AGE,NO_DOGS,NO_CATS,NO_BIRDS,NO_FISH,NO_REPTILES,GENDER) VALUES ('{name_val}',{age_val},{Dog_val},{Cat_val},{Bird_val},{Fish_val},{Reptile_val},'{gender_val}');"
        
            run_query(query,0)

def Answers():
    st.title("Answers")

    if st.button('Refresh data'):
        rows = run_query("SELECT PET , COUNT(1) AS NO_OF_PICKS FROM FAV_PET GROUP BY PET ORDER BY COUNT(1) DESC;")

        fav_pets_df = pd.DataFrame(rows , columns = ['PET','NO_OF_PICKS'])
        fav_pets_df = fav_pets_df.set_index('PET')

        # Display the results in a Streamlit table
        st.table(fav_pets_df)
        
        # Display the results in a Streamlit bar chart
        st.bar_chart(fav_pets_df)
        
        rows = run_query("SELECT ID,NAME,AGE,NO_DOGS,NO_CATS,NO_BIRDS,NO_FISH,NO_REPTILES,GENDER FROM ANSWERS;")
        
        answers_df = pd.DataFrame(rows, columns = ['ID','NAME','AGE','NO_DOGS','NO_CATS','NO_BIRDS','NO_FISH','NO_REPTILES','GENDER'])

        # Display the results in a Streamlit table
        st.table(answers_df)

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
    
def page2():
    st.title("Page 2")
    st.write("This is the second page of my app.")

    genders = ['Male', 'Female', 'Rather not say', 'Other']

    with st.form("my_form"):
        st.write("Inside the form")
        name_val = st.text_input("Name:")
        age_val = st.slider('How old are you?', 0, 130, 25)
        Dog_val = st.number_input('How many Dogs do you have')
        Cat_val = st.number_input('How many Cats do you have')
        Bird_val = st.number_input('How many Birds do you have')
        Fish_val = st.number_input('How many Fish do you have')
        Reptile_val = st.number_input('How many Reptiles do you have')
        gender_val = st.selectbox('Gender:',genders)
        
        if gender_val == 'Other':
            gender_val_other = st.text_input("Preferred Gender:")  

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        
    if submitted:
        st.write(name_val, age_val,pets_val, gender_val,gender_val_other)

    st.write("Outside the form")

def page3():
    st.title("Page 3")

    genders = ['Male', 'Female', 'Rather not say', 'Other']

    name_val = st.text_input("Name:")
    age_val = st.slider('How old are you?', 0, 130, 25)
    Dog_val = st.number_input('How many Dogs do you have')
    Cat_val = st.number_input('How many Cats do you have')
    Bird_val = st.number_input('How many Birds do you have')
    Fish_val = st.number_input('How many Fish do you have')
    Reptile_val = st.number_input('How many Reptiles do you have')
    gender_val = st.selectbox('Gender:',genders)
        
    if gender_val == 'Other':
        gender_val_other = st.text_input("Preferred Gender:")  

    st.write(name_val, age_val,Dog_val,Cat_val,Bird_val,Fish_val,Reptile_val, gender_val,gender_val_other=none)

if __name__ == "__main__":
    main()


