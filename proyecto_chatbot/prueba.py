import streamlit as st
from chatbot import predict_class, get_response, intents


st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, soy un chatbot. ¿En qué puedo ayudarte?")
    
    st.session_state.messages.append({"role": "assistant", "content": "Hola, soy un chatbot. ¿En qué puedo ayudarte?"})
    st.session_state.first_message = False

if promt := st.chat_input ("¿como puedo ayudarte?"):
    
    with st.chat_message("user"):
        st.markdown(promt)
    st.session_state.messages.append({"role": "user", "content": promt})

    #implementar el chatbot
    inst= predict_class(promt)
    res= get_response(inst,intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})