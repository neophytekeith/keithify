import streamlit as st

# Display a simple message
st.title("Heroku Deployment Test")
st.write("If you see this, it means your app is live on Heroku!")

# Optional: Add a simple input to confirm interactive functionality
user_input = st.text_input("Enter your name:")
if user_input:
    st.write(f"Hello, {user_input}!")
