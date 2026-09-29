import streamlit as st

st.header("Business Agent", text_alignment="center")

if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])


# for business query only

user_input=st.chat_input("Message....")

# need to understand massage intent first and give response

if user_input:
    
    st.session_state.messages.append({
        'role':"user",
        'content':user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    response="add lllm here" ## need to add llm

    st.session_state.messages.append({
            'role':'assistant',
            'content':response
    })

    with st.chat_message("assistent"):
        st.write(response)