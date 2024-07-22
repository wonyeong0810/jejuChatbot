from openai import OpenAI
import streamlit as st

st.title("제주사름")

client = OpenAI(api_key=st.secrets["openai_api_key"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 제주도 사투리로 대답하도록 프롬프트 엔지니어링
        jeju_prompt = f"제주도 사투리로 대답하고 ()안에 한국 표준어로 같은 말은 반복해줘:\n\n{prompt}"
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ] + [{"role": "system", "content": jeju_prompt}],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

