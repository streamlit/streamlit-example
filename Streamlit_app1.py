import streamlit as st

# Define a dictionary of valid usernames and passwords
VALID_USERS = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

def login():
    st.title("Login Page")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.success("Login successful!")
            # You can redirect to another page or show other content here after successful login
        else:
            st.error("Invalid username or password")

def main():
    login()

if __name__ == "__main__":
    main()
