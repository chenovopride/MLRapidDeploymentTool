import streamlit as st

# Set the page layout to wide
st.set_page_config(layout="wide")

# Custom CSS to mimic the Japanese master style design
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .japanese-style {
        background-color: #f4f4f9;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .download-button {
        background-color: #333;
        color: white;
        padding: 10px 24px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Creating a sidebar for inputs
with st.sidebar:
    st.header('Upload Files')
    uploaded_model = st.file_uploader("Upload your onnx model", type=["onnx", "notSupportOthers"])
    # uploaded_data = st.file_uploader("Upload test data", type=["csv", "txt", "json"])

    st.header('Configuration')
    output_format = st.selectbox("Select output format", ['onnx', 'mnn', 'tflite','tensorflow'])
    priority = st.radio("Select priority", ['Accuracy', 'Latency'])

    if st.button('Generate'):
        st.sidebar.success("Model generation started!")
        # 在这里开始调后端？后端信息传给下面st.progress(50)那里

# Main content
st.write("# Model Optimization Interface", unsafe_allow_html=True)

# Displaying progress
with st.container():
    st.write("## Model generation progress...", unsafe_allow_html=True)
    st.progress(50)
    st.write("<div class='big-font japanese-style'>Model variant1: with optimize quantization acc: 90%, latency:15ms</div>", unsafe_allow_html=True)
    st.write("<div class='big-font japanese-style'>Model variant2: with onnx simplify acc: 98%, latency:17ms</div>", unsafe_allow_html=True)
    st.write("<div class='big-font japanese-style'>Model variant3: ...... acc: 待填充, latency:待填充</div>", unsafe_allow_html=True)

    # Download button
    st.markdown("<div class='download-button'>Download All!</div>", unsafe_allow_html=True)

# Sample code area
with st.container():

    # 这里用来写gpt生成的辅助部署的代码，这个st.code竟然提供直接复制按钮，牛
    
    st.write("## Sample code for the use of the model is generated here for the user's reference", unsafe_allow_html=True)
    st.code('''
# Sample code for model usage
def load_model(model_path):
    # Your code to load the model
    pass

def test_model(data_path):
    # Your code to test the model
    pass
    ''')
