from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="💬 AI Chatbot", layout="wide")
st.title("💬 AI Chatbot")
st.markdown("Conversational AI with memory and context")

openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
persona = st.sidebar.selectbox("Persona:", ["General Assistant", "Customer Support", "Coding Expert", "Study Tutor"])

personas = {
    "General Assistant": "You are a helpful, friendly AI assistant.",
    "Customer Support": "You are a professional customer support agent. Be empathetic, solution-focused, and polite.",
    "Coding Expert": "You are an expert software engineer. Provide clean, well-commented code examples and technical explanations.",
    "Study Tutor": "You are a patient and encouraging tutor. Break down complex topics into simple steps."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Type your message..."):
    if not openai_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        client = OpenAI(api_key=openai_key)
        messages = [{"role": "system", "content": personas[persona]}] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(model="gpt-4", messages=messages)
                reply = response.choices[0].message.content
                st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
