import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
import streamlit.web.cli as stcli

def generate_pos(sentence):
    # Placeholder function for Part-of-Speech tagging
    # Replace with actual POS tagging logic
    return f"POS tags for: {sentence}"

def main():
    st.set_page_config(page_title="T2Parser", layout="wide")

    st.sidebar.title("T2Parser")
    st.sidebar.write("Select the type of input:")

    pos_sentence = st.sidebar.button("POS Sentence")
    pos_paragraph = st.sidebar.button("POS Paragraph")

    st.title("T2Parser")
    st.write("Enter your sentence")

    sentence = st.text_input("", "Như rất là giỏi luôn", max_chars=200)
    
    if st.button("Process"):
        result = generate_pos(sentence)
        st.write("Result")
        st.download_button("Download Result.txt", result, file_name="Result.txt")

    # Dummy chart for display using Echarts
    '''
    chart = (
        Line()
        .add_xaxis(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"])
        .add_yaxis("Example", [820, 932, 901, 934, 1290, 1330, 1320])
        .set_global_opts(title_opts=opts.TitleOpts(title="Example Line Chart"))
    )
    st_pyecharts(chart)
    '''

if __name__ == "__main__":
    main()
