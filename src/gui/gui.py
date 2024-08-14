import streamlit as st
from pos_execute import get_pos_data_old, fetch_data_id, fetch_data_id_file, get_pos_data, generate_table_and_chunks
from constants import POS_MEANINGS

st.set_page_config(page_title="T2 Parser", page_icon=":rocket:", layout="wide")

# MAIN SECTION
with st.container():
    st.divider()
    st.header("Let's Get Started")

    # left_column_new, right_column_new = st.columns([7, 3])
    # with left_column_new:
    search_input = st.text_input(
                "Found your result with data_id",
                placeholder="Enter your data_id here...",
                max_chars=100
    )

    if st.button('Search'):
        data_id_search = search_input
        if len(data_id_search) == 0:
            st.error("Please enter a valid data_id")
            
        
        if data_id_search:
            data_analyze_search, err_search = get_pos_data(data_id_search)
            print('HELLO WORLD', data_analyze_search)

            if err_search:
                st.error(f"We cannot find any data_id: {data_id_search}. Please try again. Detailed error: {err_search}")
                #st.stop()
            else:
                details_search = data_analyze_search.get("details", [])
            
                if len(details_search) == 0 :
                    st.error("An internal error occurred. Please retry the request again")
                    #st.stop()
                pos_data_search, colored_chunks_search = generate_table_and_chunks(data_analyze_search)
            
                if not pos_data_search.empty:
                    table_column, chunks_column = st.columns(2)

                    # Hiển thị kết quả phân tích POS
                    with table_column:
                        st.write("Results of POS analysis:")
                        #st.write('Data ID:', data_id)

                        
                        # Convert DataFrame to HTML for styling
                        html = pos_data_search.to_html(escape=False, index=False)
                        
                        st.markdown(html, unsafe_allow_html=True)

                    # Hiển thị chuỗi POS đã được tô màu
                    with chunks_column:
                            st.write("POS of tag")
                            st.markdown(f"Data ID: <p style='color:yellow;'>{data_id_search}</p>", unsafe_allow_html=True)
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
                                    {colored_chunks_search}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                else: 
                    st.error(f"Cannot retrieve data_id: {data_id_search}")
    st.divider()
    st.subheader("If you don't have data_id, please input your text or upload your file")

    # PHẦN NÀY DÙNG ĐỂ NHẬP INPUT VÀ CHỌN MODEL NẾU NGƯỜI DÙNG KHÔNG CÓ SẴN DATA_ID

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
            type=['txt']
        )

    # MODEL SELECTION
    model_mapping = {
        'underthesea': 'underthesea',
        'VnCoreNLP': 'vncorenlp'
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
                
                data_analyze = get_pos_data_old(data_id)

                details = data_analyze.get("details", [])
                
                if len(details) == 0 :
                    st.error("An internal error occurred. Please retry the request again")
                
                pos_data, colored_chunks = generate_table_and_chunks(data_analyze)
                
                if not pos_data.empty:
                    table_column, chunks_column = st.columns(2)

                    # Hiển thị kết quả phân tích POS
                    with table_column:
                        st.write("Results of POS analysis:")
                        #st.write('Data ID:', data_id)

                        
                        
                        # Convert DataFrame to HTML for styling
                        html = pos_data.to_html(escape=False, index=False)
                        
                        st.markdown(html, unsafe_allow_html=True)

                    # Hiển thị chuỗi POS đã được tô màu
                    with chunks_column:
                        st.write("POS of tag")
                        st.markdown(f"Data ID: <p style='color:yellow;'>{data_id}</p>", unsafe_allow_html=True)
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