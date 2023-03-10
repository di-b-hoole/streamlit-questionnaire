import streamlit as st
import snowflake.connector
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
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

def navigation():
    choice = st.session_state.menu
    

def main():
    st.title("Power Hour 2023-03-08")
    
    # Set up initial form to get input values
    st.write('Please enter name:')
    name = st.text_input('Name:', key="name")

    st.write(st.session_state.name)

    # Side bar
    menu = ["Favourite Pet", "Questions", "Answers","Predictions"]

    choice = st.sidebar.selectbox("Select a page", menu)
    #st.sidebar.selectbox("Select a page", menu, on_change=navigation, key='menu')
    
    if choice == "Favourite Pet":
        Fav_Pet()
    elif choice == "Questions":
        Questions()
    elif choice == "Answers":
        Answers()
    elif choice == "Predictions":
        Predictions()


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
    st.title("Please give us the actual values below :)")

    with st.form("my_form"):
        
        Dog_val = st.number_input('How many Dogs do you have', min_value=0, max_value=100, value=0, step=1)
        Cat_val = st.number_input('How many Cats do you have', min_value=0, max_value=100, value=0, step=1)
        Bird_val = st.number_input('How many Birds do you have', min_value=0, max_value=100, value=0, step=1)
        Fish_val = st.number_input('How many Fish do you have', min_value=0, max_value=100, value=0, step=1)
        Reptile_val = st.number_input('How many Reptiles do you have', min_value=0, max_value=100, value=0, step=1)

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

def prediction_model(birth,dwell,gen,living):
    
    # Select the columns we want to use for prediction
    amounts = data[['DOG_AMOUNT', 'CAT_AMOUNT', 'FISH_AMOUNT', 'BIRD_AMOUNT', 'REPTILE_AMOUNT','CAT_IND','DOG_IND','FISH_IND','BIRD_IND','REPTILE_IND']]
    dat = data[['BIRTH_YEAR','DWELLING_TYPE','GENDER','LIVING_AREA']]

    # Construct dataframe from form response
    data_from_form = [{'BIRTH_YEAR': birth,
                       'DWELLING_TYPE': dwell,
                       'GENDER':gen,
                       'LIVING_AREA':living}]
    # Create a decision tree regression model
    model = DecisionTreeRegressor() 
    # Fit the model to the training data
    st.cache_resource(model.fit(dat, amounts))
    y_pred = model.predict(data_from_form)
    for i in y_pred:
        output_data = i

    #query = f"INSERT INTO ANSWERS (NAME,AGE,NO_DOGS,NO_CATS,NO_BIRDS,NO_FISH,NO_REPTILES,GENDER) VALUES ({age_val},{Dog_val},{Cat_val},{Bird_val},{Fish_val},{Reptile_val},'{gender_val}');"
        
            #run_query(query,0)


    return   f'''Amount of dogs:{output_data[0]}
                     Amount of cats:{output_data[1]}
                     Amount of fish:{output_data[2]}
                     Amount of birds:{output_data[3]}
                     Amount of reptiles:{output_data[3]}
                  '''

def Predictions():
    st.title("Prediction")

    results = run_query('SELECT DISTINCT GENDER from POWER_HOUR.PUBLIC.GENDER')
    genders = [str(row[0]) for row in results]

    results = run_query('SELECT DISTINCT LIVING_AREA from POWER_HOUR.PUBLIC.LIVING_AREA')
    living_area = [str(row[0]) for row in results]

    results = run_query('SELECT DISTINCT DWELLING_TYPE from POWER_HOUR.PUBLIC.DWELLING_TYPE')
    dwelling_type = [str(row[0]) for row in results]

    with st.form("Predictions Form"):
        gender_val = st.selectbox('Gender:',genders)
        age_val = st.number_input(
            'Enter your birth year between 1942 and 2004:',
            min_value=1942,
            max_value=2004,
            step=1,
        )
        living_area_val = st.selectbox('Living Area:',living_area)
        dwelling_type_val = st.selectbox('Dwelling Type:',dwelling_type)
        
        submitted = st.form_submit_button("Submit")

    if submitted:
        
        gender_val_int = run_query(f"SELECT ID FROM PUBLIC.GENDER WHERE GENDER = '{gender_val}';")[0][0]
        living_area_val_int = run_query(f"SELECT ID FROM PUBLIC.LIVING_AREA WHERE LIVING_AREA = '{living_area_val}';")[0][0]
        dwelling_type_val_int = run_query(f"SELECT ID FROM PUBLIC.DWELLING_TYPE WHERE DWELLING_TYPE = '{dwelling_type_val}';")[0][0]
        
        st.write('Gender:',gender_val,gender_val_int)
        st.write('Birth Year:',age_val)
        st.write('Living Area:',living_area_val, living_area_val_int)
        st.write('Dwelling Type:',dwelling_type_val, dwelling_type_val_int)

        # Streamlit elements
        st.title('Predictions')
        mark_body = 'Based of the information given through we predict the following:'
        st.write(mark_body)
        st.write(prediction_model(age_val,dwelling_type_val_int,gender_val_int,living_area_val_int))

   

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


