import os
import streamlit as st
from app import chatWithLLM

st.header("Business Agent")

# set SHOW_SILENT_HINT=1 in .env while developing to SEE when the bot stayed silent
SHOW_HINT = os.getenv("SHOW_SILENT_HINT", "0") == "1"

if "messages" not in st.session_state:
    st.session_state.messages = []

# if "llm_history" not in st.session_state:
#     st.session_state.llm_history = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

user_input = st.chat_input("Ask about products, price, stock ...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    reply = chatWithLLM(user_input, history=st.session_state.messages)
    

    if reply is None: 
        # st.write("not model response")  # not business related -> show NOTHING, save nothing
        if SHOW_HINT:
            st.caption("(dev) bot stayed silent: not a business message")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)