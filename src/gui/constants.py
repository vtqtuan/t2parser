# API URL
API_URL = "http://localhost:8000/parse"

# Bảng mã màu
POS_MEANINGS = {
    "A": ("Tính từ", "#FFA500"),       # orange
    "Ab": ("Tính từ mượn", "#FFDAB9"),  # lightorange
    "B": ("Từ mượn", "#a6f768"),       # xanh chuối
    "C": ("Liên từ", "#90EE90"),       # lightgreen
    "Cc": ("Liên từ đẳng lập", "#90EE90"),
    "CH": ("Dấu câu", "#87CEEB"),       # skyblue
    "E": ("Giới từ", "#dbcecf"),       # lightpink
    "Fw": ("Từ nước ngoài", "#ADD8E6"), # lightblue
    "FW": ("Từ nước ngoài", "#ADD8E6"),
    "I": ("Thán từ", "#800080"),       # purple
    "L": ("Định từ", "#FFB6C1"),       # lightpink
    "M": ("Số từ", "#F08080"),         # lightcoral
    "N": ("Danh từ", "#b9faff"),       # thiên thanh
    "Nb": ("Danh từ mượn", "#FA8072"),  # salmon
    "Nc": ("Danh từ chỉ loại", "#ecb3ff"),
    "Ne": ("Danh từ chỉ loại", "#ecb3ff"),
    "Ni": ("Danh từ kí hiệu", "#ad66ff"),
    "Np": ("Danh từ riêng", "#ffdfba"), # lightyellow
    "NNP": ("Danh từ riêng", "#ffdfba"),
    "Ns": ("Danh từ", "#FA8072"),
    "Nu": ("Danh từ đơn vị", "#8B0000"),
    "Ny": ("Danh từ viết tắt", "#8B0000"),
    "P": ("Đại từ", "#67d690"),       # lightgrey
    "R": ("Phó từ", "#E0FFFF"),       # lightcyan
    "S": ("Phó từ", "#E0FFFF"),
    "T": ("Trợ từ", "#ff8e42"),       # light orange
    "V": ("Động từ", "#FFFF00"),       # yellow
    "Vb": ("Động từ mượn", "#FFFFE0"),  # lightyellow
    "Vy": ("Động từ viết tắt", "#FFFFE0"),
    "X": ("Không phân loại", "#D3D3D3"), # lightgrey
    "Y": ("Unknown", "#D3D3D3"),
    "Z": ("Yếu tố cấu tạo từ", "#f3a2f5")
}
