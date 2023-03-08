import streamlit as st

def main():
    st.set_page_config(page_title="My Streamlit App")

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

def page1():
    st.title("Page 1")
    st.write("This is the first page of my app.")

def page2():
    st.title("Page 2")
    st.write("This is the second page of my app.")

if __name__ == "__main__":
    main() #test
