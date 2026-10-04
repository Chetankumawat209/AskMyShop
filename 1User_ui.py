# import os
# import streamlit as st
# from llm import chatWithLLM

# st.header("Business Agent")

# # set SHOW_SILENT_HINT=1 in .env while developing to SEE when the bot stayed silent
# SHOW_HINT = os.getenv("SHOW_SILENT_HINT", "0") == "1"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for m in st.session_state.messages:
#     with st.chat_message(m["role"]):
#         st.write(m["content"])

# user_input = st.chat_input("Ask about products, price, stock ...")
# api_key = st.text_input(
#     "Enter your Gemini API key",
#     type="password"
# )

# user_input = st.chat_input("Ask about products, price, stock ...")

# if user_input and api_key:
#     with st.chat_message("user"):
#         st.write(user_input)
#     reply = chatWithLLM(user_input, history=st.session_state.messages)
    

#     if reply is None: 
#         #  # not business related -> show NOTHING, save nothing

#         # st.session_state.messages.append({"role": "user", "content": user_input})
#         # st.session_state.messages.append({"role": "assistant", "content": reply})
#         # with st.chat_message("assistant"):
#         #     st.write()     # not model response


#         if SHOW_HINT:
#             st.caption("(dev) bot stayed silent: not a business message")
#     else:
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         st.session_state.messages.append({"role": "assistant", "content": reply})
#         with st.chat_message("assistant"):
#             st.write(reply)



import os
import streamlit as st
from llm import chatWithLLM

st.header("Business Agent")

# Set SHOW_SILENT_HINT=1 in .env while developing
SHOW_HINT = os.getenv("SHOW_SILENT_HINT", "0") == "1"


# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])


# -----------------------------
# Gemini API Key
# -----------------------------
api_key = st.text_input(
    "Enter your Gemini API key",
    type="password"
)


# -----------------------------
# Customer message
# -----------------------------
user_input = st.chat_input(
    "Ask about products, price, stock ..."
)


# -----------------------------
# Process message
# -----------------------------
if user_input:

    if not api_key:
        st.warning("Please enter your Gemini API key first.")

    else:

        with st.chat_message("user"):
            st.write(user_input)

        reply = chatWithLLM(
            user_input,
            history=st.session_state.messages,
            api_key=api_key
        )

        if reply is None:

            # Not business-related → stay silent
            if SHOW_HINT:
                st.caption(
                    "(dev) bot stayed silent: not a business message"
                )

        else:

            # Save conversation
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

            with st.chat_message("assistant"):
                st.write(reply)