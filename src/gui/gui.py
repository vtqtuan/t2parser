import streamlit as st
from pos_execute import fetch_data_id, fetch_data_id_file, get_pos_data, generate_table_and_chunks
from constants import POS_MEANINGS

st.set_page_config(page_title="Streamline Analyst", page_icon=":rocket:", layout="wide")

# MAIN SECTION
with st.container():
    st.divider()
    st.header("Let's Get Started")

    left_column, right_column = st.columns([6, 4])

    # INPUT SECTION
    with left_column:
        # text_input = st.text_input(
        #     "Input the text you want to POS",
        #     placeholder="Enter here...",
        # )

        text_input = st.text_area(
            "Input the text you want to POS analyze",
            placeholder="Enter anything here...",
        )

        uploaded_file = st.file_uploader(
            "Choose a data file. Your data will be kept secretly and securely.", 
            accept_multiple_files=False, 
            type=['csv', 'json', 'xls', 'xlsx', 'txt']
        )

    # MODEL SELECTION
    model_mapping = {
        'undertheseanlp model': 'underthesea',
        'vnCoreNLP model': 'vncorenlp'
    }
    with right_column:
        SELECTED_MODEL = st.selectbox(
            'Which model you want to use for POS analysis?',
            model_mapping.keys()
        )
        
        actual_model_value = model_mapping[SELECTED_MODEL]
    
        st.write(f'Model selected: :green[{SELECTED_MODEL}]')

    # BUTTON Analyze EXECUTE
    if st.button('Analyze'):
        st.divider()

        if len(text_input) > 255:
                user_input = text_input[:255]
                st.error("The input exceeds 255 characters. Please try again")
                st.stop()  # Stop further execution
                  
        # Check if the user has provided both text and file
        if (text_input and uploaded_file) or (not text_input and not uploaded_file):
            st.warning("Please provide only one input: either text or file, not both or none.")
        #Limit the input to 255 characters
        else:
            if text_input:
                # Gọi API để lấy data_id từ văn bản
                data_id, err = fetch_data_id(text_input, actual_model_value)
            elif uploaded_file:
                # Gọi API để lấy data_id từ file tải lên
                data_id, err = fetch_data_id_file(uploaded_file, actual_model_value)

            if data_id:
                # Sử dụng data_id để lấy dữ liệu POS
                
                data_analyze = get_pos_data(data_id)

                details = data_analyze.get("details", [])
                
                if len(details) == 0 :
                    st.error("An internal error occurred. Please retry the request again")
                
                pos_data, colored_chunks = generate_table_and_chunks(data_analyze)
                
                if not pos_data.empty:
                    table_column, chunks_column = st.columns(2)

                    # Hiển thị kết quả phân tích POS
                    with table_column:
                        st.write("Results of POS analysis:")
                        
                        # Convert DataFrame to HTML for styling
                        html = pos_data.to_html(escape=False, index=False)
                        
                        st.markdown(html, unsafe_allow_html=True)

                    # Hiển thị chuỗi POS đã được tô màu
                    with chunks_column:
                        st.write("POS of tag")
                        st.markdown(
                            f"""
                            <div style="
                                background-color: rgb(38, 39, 48); 
                                border: 1px solid #d0d0d0; 
                                border-radius: 5px; 
                                padding: 10px; 
                                min-height: 150px; 
                                max-height: 300px; 
                                overflow-y: auto;
                                font-family: sans-serif;
                            ">
                                {colored_chunks}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.error(f"Failed to retrieve data_id. Error: {err}")