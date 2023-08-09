import streamlit as st

# Define a dictionary of valid usernames and passwords
VALID_USERS = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

# Fake data for the dashboard
fake_data = {
    'Total Sales': 123456,
    'Profit': 54321,
    'Expenses': 98765,
    'Customers': 789,
    'Products': 456
}

def login():
    st.title("Login Page")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.success("Login successful!")
            dashboard()
        else:
            st.error("Invalid username or password")

def dashboard():
    st.title("Dashboard")
    st.write("Welcome to the Dashboard! Here are some fake numbers:")

    for metric, value in fake_data.items():
        st.metric(label=metric, value=value)

def main():
    login()

if __name__ == "__main__":
    main()
