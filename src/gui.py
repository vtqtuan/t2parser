import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Line
import streamlit.web.cli as stcli
import os

def process_pos(sentence):
    # Placeholder function for T2PARSER
    # Replace this with actual T2PARSER logic
    return f"Processed POS tags for: {sentence}"

def main():
    st.set_page_config(page_title="T2PARSER App", layout="wide")

    # Sidebar navigation
    # st.sidebar.title("T2PARSER App")
    # page = st.sidebar.radio("Select Page", ["POS Sentence", "POS Paragraph"])
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "POS Sentence"

    # Sidebar navigation with buttons
    st.sidebar.title("T2PARSER App")
    
    if st.sidebar.button("POS Sentence"):
        st.session_state.page = "POS Sentence"
    if st.sidebar.button("POS Paragraph"):
        st.session_state.page = "POS Paragraph"

    if st.session_state.page == "POS Sentence":
        st.title("T2PARSER - Sentence")
        st.write("Enter your sentence")

        sentence = st.text_input("", "Như rất là giỏi luôn", max_chars=200)
        
        if st.button("Process"):
            result = process_pos(sentence)
            st.write("Result")
            st.download_button("Download Nhuratlagioi_result.txt", result, file_name="Nhuratlagioi_result.txt")

    elif st.session_state.page == "POS Paragraph":
        st.title("T2PARSER - Paragraph")
        st.write("Drag and drop your file")

        
        # Đoạn code này để upload chỉ 1 file
        #uploaded_file = st.file_uploader("Choose a file", type=["txt"],accept_multiple_files=True)
        #if uploaded_file is not None:
            #st.write(f"Uploaded file: {uploaded_file.name}")
            #content = uploaded_file.read().decode("utf-8")

            #if st.button("Process"):
                #result = process_pos(content)
                #st.write("Result")
                #st.download_button("Download NHURATLAGIOI_RESULT.txt", result, file_name="NHURATLAGIOI_RESULT.txt")

        # Đoạn code này để upload nhiều file - File uploader to allow multiple file uploads
        uploaded_files = st.file_uploader("Choose files", type=["txt"], accept_multiple_files=True)
        
        # Check if any files are uploaded
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                st.write(f"Uploaded file: {uploaded_file.name}")
                # Read the content of the uploaded file
                content = uploaded_file.read().decode("utf-8")

                # Process button for each uploaded file
                if st.button(f"Process {uploaded_file.name}"):
                    result = process_pos(content)
                    st.write("Result")
                    # Download button for the processed result of each file
                    st.download_button(f"Download {uploaded_file.name}_RESULT.txt", result, file_name=f"{uploaded_file.name}_RESULT.txt")

if __name__ == "__main__":
    main()