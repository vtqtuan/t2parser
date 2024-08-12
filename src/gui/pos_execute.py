import requests
import pandas as pd
from constants import POS_MEANINGS, API_URL


# Hàm gọi API để lấy data_id
def fetch_data_id(text_input, model):
    encoded_data = text_input.encode('utf-8')
    headers = {
        'Content-Type': 'text/plain; charset=utf-8',
        'model': model  # Thêm giá trị model vào header
    }
    
    response = requests.post(API_URL, data=encoded_data, headers=headers)
    
    try:
        response.raise_for_status()
        data = response.json()
        return data.get("data_id"), None
    except Exception as err:
        return None, err
    
def fetch_data_id_file(uploaded_file, model):
    headers = {
        'model': model  # Thêm giá trị model vào header
    }

    # Prepare the file to be sent as form-data
    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    
    response = requests.post(f"{API_URL}/file", files=files, headers=headers)
    
    try:
        response.raise_for_status()
        data = response.json()
        return data.get("data_id"), None
    except Exception as err:
        return None, err


    
# Hàm gọi API để lấy dữ liệu POS
def get_pos_data(data_id):
    url = f"{API_URL}/{data_id}"
    response = requests.get(url)
    
    try:
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as err:
        return None, err


# từ dữ liệu trả về, tạo bảng và câu mới theo mã màu
def generate_table_and_chunks(data):
    details = data.get("details", [])
    unique_tags = list({(item["tag"], POS_MEANINGS.get(item["tag"], ("Unknown", "black"))[0]) for item in details})
    
    # Create a DataFrame with POS_Tag, Meaning, and Color
    pos_data = pd.DataFrame(unique_tags, columns=["POS_Tag", "Meaning"])
    pos_data['Color'] = pos_data['POS_Tag'].map(lambda x: POS_MEANINGS.get(x, ("Unknown", "black"))[1])
    
    # Apply color to both POS_Tag and Meaning columns
    pos_data['POS_Tag'] = pos_data.apply(lambda row: f"<span style='color:{row['Color']}'>{row['POS_Tag']}</span>", axis=1)
    pos_data['Meaning'] = pos_data.apply(lambda row: f"<span style='color:{row['Color']}'>{row['Meaning']}</span>", axis=1)
    
    # Reorder columns to include the colored versions
    pos_data = pos_data[['POS_Tag', 'Meaning']]
    
    # Generate colored chunks
    chunks = " ".join([f"<span style='color:{POS_MEANINGS[item['tag']][1]}'>{item['chunk']}</span>" for item in details])
    
    return pos_data, chunks