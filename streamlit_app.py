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
        
        if expectResult == 2:
            # Get the column headers
            headers = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            df = pd.DataFrame(results, columns=headers)
            return df
        if expectResult != 0:
            return cur.fetchall()

def navigation():
    choice = st.session_state.menu

    if choice == "Main":
        v = True
    elif choice == "Favourite Pet":
        Fav_Pet()
    elif choice == "Predictions":
        Predictions()
    elif choice == "Actuals":
        Questions()
    elif choice == "Answers":
        Answers()
    
def main():
    st.title("Power Hour 2023-03-08")
    
    # Set up initial form to get input values
    st.write('Please enter name:')
    name = st.text_input('Name:', key="name")

    st.write(st.session_state.name)

    # Side bar
    menu = ["Main","Predictions","Favourite Pet", "Actuals", "Answers"]

    choice = st.sidebar.selectbox("Select a page", menu)
    
    if choice == "Main":
        v = True
    elif choice == "Favourite Pet":
        Fav_Pet()
    elif choice == "Predictions":
        Predictions()
    elif choice == "Actuals":
        Questions()
    elif choice == "Answers":
        Answers()
    
def Fav_Pet():
    st.title("Choose your favourite pet")

    pets = ["Dog", "Cat", "Bird", "Fish", "Reptile"]
    favourite_pet = st.selectbox("Select you favourite pet:", pets)

    # Define the SQL query and parameters
    query = f"INSERT INTO FAV_PET (NAME,PET) VALUES ('{st.session_state.name}','{favourite_pet}');"

    # Execute the query
    if st.button('Submit data'):
        if 'name' in st.session_state:
            run_query(query,0)
            st.write(favourite_pet)
        else:
            st.write("Please enter a Name!")

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
            if 'name' in st.session_state:
                query = f"INSERT INTO ANSWERS (NAME,NO_DOGS,NO_CATS,NO_BIRDS,NO_FISH,NO_REPTILES,IS_PREDICTION) VALUES ('{st.session_state.name}',{Dog_val},{Cat_val},{Bird_val},{Fish_val},{Reptile_val},0);"
        
                run_query(query,0)

                st.write('Amount of Dogs:',Dog_val)
                st.write('Amount of Cats:',Cat_val)
                st.write('Amount of Fish:',Fish_val)
                st.write('Amount of Birds:',Bird_val)
                st.write('Amount of Reptiles:',Reptile_val)
            else:
                st.write("Please enter a Name!")
            
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
    
    # pull data from snowflake
    data = run_query('select * from POWER_HOUR.PUBLIC.TRANSFORMED_HIST_NEW where dwelling_type is not null and gender is not null  and living_area is not null',2)
    
    # Select the columns we want to use for prediction
    amounts = data[['DOG_AMOUNT', 'CAT_AMOUNT', 'FISH_AMOUNT', 'BIRD_AMOUNT', 'REPTILE_AMOUNT','CAT_IND','DOG_IND','FISH_IND','BIRD_IND','REPTILE_IND']]
    dat = data[['BIRTH_YEAR','DWELLING_TYPE','GENDER','LIVING_AREA']]

    # Construct dataframe from response
    data_from_form = { 'BIRTH_YEAR': [birth],
                       'DWELLING_TYPE': [dwell],
                       'GENDER':[gen],
                       'LIVING_AREA':[living]}
    data_from_form = pd.DataFrame(data_from_form)
    # Create a decision tree regression model
    model = DecisionTreeRegressor() 
    # Fit the model to the training data
    model.fit(dat, amounts)
    y_pred = model.predict(data_from_form)
    for i in y_pred:
        output_data = i

    query = f"INSERT INTO ANSWERS (NAME,NO_DOGS,NO_CATS,NO_BIRDS,NO_FISH,NO_REPTILES,IS_PREDICTION) VALUES ('{st.session_state.name}',{output_data[0]},{output_data[1]},{output_data[3]},{output_data[2]},{output_data[4]},1);"
        
    run_query(query,0)

    return [output_data[0],output_data[1],output_data[2],output_data[3],output_data[4]]
                #f''' Amount of  dogs:{output_data[0]}
                #     Amount of cats:{output_data[1]}
                #     Amount of fish:{output_data[2]}
                #     Amount of birds:{output_data[3]}
                #     Amount of reptiles:{output_data[4]}
                # '''

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
        
        #st.write('Gender:',gender_val,gender_val_int)
        #st.write('Birth Year:',age_val)
        #st.write('Living Area:',living_area_val, living_area_val_int)
        #st.write('Dwelling Type:',dwelling_type_val, dwelling_type_val_int)

        query = f"INSERT INTO DEMOGRAPHICS (NAME,GENDER,LIVING_AREA,DWELLING_TYPE,BIRTH_YEAR) VALUES ('{st.session_state.name}','{gender_val}','{living_area_val}','{dwelling_type_val}',{age_val});"
        
        run_query(query,0)

        # Streamlit elements
        st.title('Predictions')
        mark_body = 'Based of the information given through we predict the following:'
        st.write(mark_body)
        prediction = prediction_model(age_val,dwelling_type_val_int,gender_val_int,living_area_val_int)

        st.write('Amount of Dogs:',prediction[0])
        st.write('Amount of Cats:',prediction[1])
        st.write('Amount of Fish:',prediction[2])
        st.write('Amount of Birds:',prediction[3])
        st.write('Amount of Reptiles:',prediction[4])

if __name__ == "__main__":
    main()


