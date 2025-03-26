import streamlit as st
import ollama 
import os
import re
import shelve

# Streamlit application

def run():

    USER_AVATAR = "😎"
    BOT_AVATAR = "🤖"


    # Load chat history from shelve file
    def load_chat_history(chat_history_model):
        with shelve.open(chat_history_model) as db:
            return db.get("messages", [])


    # Save chat history to shelve file
    def save_chat_history(chat_history_model, messages):
        with shelve.open(chat_history_model) as db:
            db["messages"] = messages


    # Image , icons to decorate
    logo_path = "./static/logo_a.jpg"
    img_path = "./static/logo_b.jpg"

    # messages init
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.model = "ollama models" 
    list_of_llms = [model.model for model in ollama.list().models]
    list_of_llms.insert(0,"ollama models")
    
    sidebar = st.sidebar
    with sidebar:
        cols = st.columns(10)
        st.image(logo_path, width=100)
 
        # Selectbox for LLM
        #list_of_llms.insert(0,"ollama models")
        selected_model = st.selectbox("Local LLMs:", list_of_llms)

        st.session_state.model = selected_model

        pattern = r'^[^:]+'
        match = re.match(pattern, selected_model)
        short_model_name = match.group()

        model_id = "./db/chat_with_" + short_model_name

        # Initialize or load chat history
        if "messages" not in st.session_state:
            st.session_state.messages = load_chat_history(model_id)

        if st.session_state.model != "ollama models":
            st.markdown("\n")  
            st.markdown("""___""")
            st.markdown("\n")  

            if st.button("Delete Chat with " + match.group()):
                st.session_state.messages = []
                save_chat_history(model_id,[])

    cols = st.columns(10)   

    if st.session_state.model == "ollama models":
        st.markdown("<h2 style='text-align: left;'><i>Select your local LLM</i></h2>",
                    unsafe_allow_html=True)
    else: 
        with cols[4]:   
            st.markdown("\n") 
            st.image(img_path, width=100)
            st.markdown("\n") 
        st.markdown("<h2 style='text-align: center;'><i>" + st.session_state.model + 
                    "</i></h2>", unsafe_allow_html=True)

    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if st.session_state.model != "ollama models":

        # Main chat interface
        if prompt := st.chat_input("Talk to your model...", max_chars=0):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                full_response = ""
                for response in ollama.chat(
                    model=selected_model,
                    messages=st.session_state["messages"],
                    stream=True
                ):
                    full_response +=response['message']['content'] or ""
                    message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Save chat history after each interaction
        save_chat_history(model_id,st.session_state.messages)

if __name__ == "__main__":
    run()