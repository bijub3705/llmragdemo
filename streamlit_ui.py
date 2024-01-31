import streamlit as st
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
from llm import query
from io import StringIO
from vector_db import load_data, get_chunk_data

def init_page() -> None:
  st.set_page_config(
    page_title="Test Chatbot"
  )
  st.header("Test Chatbot")
  st.sidebar.title("Options")

def init_messages() -> None:
  clear_button = st.sidebar.button("Clear Conversation", key="clear")
  if clear_button or "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [
      SystemMessage(
        content="""You are a helpful AI assistant. Use the following context to answer the question at the end. Stop when you've answered the question. Do not generate any more than that.
        Consider the following information to answer questions: \n
        """
      )
    ]
  upload_button = st.sidebar.button("Upload document", key="upload")
  if upload_button:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
    # To read file as bytes:
      stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
      print(stringio)
     

def get_answer(prompt) -> str:
  return query(prompt)

def get_current_prompt(user_input)-> None:
    chunked_vector_data = get_chunk_data(user_input)
    #print(chunked_vector_data)
    prompt_system_message = f"""
    {chunked_vector_data}
    """
    st.session_state.messages.append(SystemMessage(content=prompt_system_message))
    st.session_state.messages.append(HumanMessage(content=user_input))
    prompt = ""
    messages = st.session_state.get("messages", [])
    for message in messages: 
        if isinstance(message, SystemMessage):
            prompt += message.content + "\n"
        elif isinstance(message, AIMessage):
            prompt += message.content + "\n"
        elif isinstance(message, HumanMessage):
            prompt += "Question :" +message.content + "? \n"
    
    print(prompt)
    return prompt

def main() -> None:
  load_data()
  init_page()
  init_messages()

  if user_input := st.chat_input("Ask your question!"):
    with st.spinner("AI assistant is finding the answer for you ..."):
      updated_prompt = get_current_prompt(user_input)
      answer = get_answer(updated_prompt)
      #print(answer)
    st.session_state.messages.append(AIMessage(content=answer))

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
             with st.chat_message("user"):
                st.markdown(message.content)

if __name__ == "__main__":
  main()