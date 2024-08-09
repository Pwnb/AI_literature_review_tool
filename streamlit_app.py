import streamlit as st
from openai import OpenAI
import PyPDF2
from docx import Document

# Show title and description.
st.title("📄 AI Literature Review Project")
st.write(
    "Upload the article below and ask a question about it. "
    "To use this service, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, .pdf, .docx, .doc)", type=("txt", "md", "pdf", "docx", "doc")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file based on its type
        if uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            document = ""
            for page in reader.pages:
                document += page.extract_text()
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            document = "\n".join([para.text for para in doc.paragraphs])
        else:
            document = uploaded_file.read().decode()

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)


