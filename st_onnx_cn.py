import streamlit as st
import subprocess
import webbrowser
from varient_generate_select import *
import time

# 主页面 - 日志信息
# Main content
st.write("## MLRapidDeploymentTool: Optimize Your AI Models and Convert to the Target Format <br><br>", unsafe_allow_html=True)
# st.subheader('右边主要栏目：')
st.text('使用方法：xxxxxx')
st.markdown("---")

def visualize_model(model_path):

    print("Visualize this model")
    # 在后台运行 Netron 命令
    subprocess.Popen(['netron', model_path, '--host', 'localhost', '--port', '8080'])

    # with st.sidebar:

    #     # 提示用户即将打开新的网页
    #     st.write("正在打开Netron...如果没有自动打开，请点击下方的链接：")
        
    #     # 在新标签页中打开 Netron 界面
    #     st.markdown("[Open Netron](http://localhost:8080)", unsafe_allow_html=True)

    # 可选：Python自动打开网页（取决于用户的浏览器设置和权限）
    webbrowser.open_new_tab("http://localhost:8080")

def model_variant_generate(input_model_path, out_format = "onnx", quant = False, optimize = False, output_model_dir = "converted_models"):
    
    # 调用后端
    model_variant_generate_backend(input_model_path, out_format, quant, optimize, output_model_dir)
    display_progress_info()
    display_sample_code()


def display_the_sidebar():
    
    with st.sidebar:

        # 侧边栏 - 模型上传
        st.header('操作栏')
        uploaded_model = st.file_uploader("上传您的.onnx模型", type=["onnx"])

        uploaded_model_path = None

        # 如果上传了model
        if uploaded_model is not None:
            file_path = "onnx_uploads/temp_" + uploaded_model.name
            uploaded_model_path = file_path

            # 打开一个新的文件写入上传的文件内容
            with open(file_path, "wb") as f:
                # uploaded_file.getvalue() 读取文件内容
                f.write(uploaded_model.getvalue())

            # print("type uploaded_model:", type(uploaded_model)) # <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
            st.button('查看模型结构', on_click = visualize_model, args=(file_path,))

        # 侧边栏 - 基础选项
        st.sidebar.subheader('基础选项')
        model_format = st.sidebar.selectbox('模型转换格式选择', ['onnx', 'mnn', 'tflite', 'tf', '...'])
        quantize_model = st.sidebar.checkbox('是否需要模型量化')
        optimize_model = st.sidebar.checkbox('是否需要经过简单优化')

        # 工具提示
        if quantize_model:
            st.sidebar.info('模型量化会减小模型体积但是会损失精度')
        if optimize_model:
            st.sidebar.info('简单优化仅消除冗余操作，不影响精度')

        st.markdown("---")
        # 侧边栏 - 高级选项
        if st.sidebar.checkbox('高级选项'):
            st.caption("选择后，软件可自动帮您生成所有可能的优化结果，并自动测试推理延迟，返回最优模型。", unsafe_allow_html=True)
            st.sidebar.text_input('填写模型输入尺寸')
            optimization_priority = st.sidebar.radio(
                '更注重准确性还是延迟', ['准确性', '延迟']
            )
        
        if st.button('Generate!', type="primary", 
                     on_click = model_variant_generate,
                     args=(uploaded_model_path, model_format, quantize_model, optimize_model, )
                     ):
            if uploaded_model_path == None:
                st.sidebar.info('您还未选择模型！')
            else:
                st.sidebar.success("Model generation started! May need sometime...")

display_the_sidebar()



def display_progress_info():
    # Displaying progress
    # with st.container():
        # st.write("Model generation progress...", unsafe_allow_html=True)
    with st.spinner('Model generation progress...'):
        time.sleep(5)
    st.success('Done!')

    opt_model_path = "onnx_models\model_c2_dep4_db18_gun_opt.onnx"
    download_generated_model(opt_model_path)

    # TODO2: 点击这个button后 display_progress_info 里面的所有信息就不见了
    st.button('查看生成的模型结构', on_click = visualize_model, args=(opt_model_path,))

def download_generated_model(model_path):

    # TODO1: 点击这个button后 display_progress_info 里面的所有信息就不见了
    # 指定ONNX模型文件的路径
    file_path = model_path

    # 读取ONNX文件的内容
    with open(file_path, "rb") as file:
        btn = st.download_button(
                label="Download the optimized model",
                data=file,
                file_name="your_model.onnx",
                mime="application/octet-stream"
            )
        

def display_sample_code():

    # Sample code area
    with st.container():

        # 这里用来写gpt生成的辅助部署的代码，这个st.code竟然提供直接复制按钮，牛
        
        st.write("### Sample code for the use of the model is generated here for the user's reference", unsafe_allow_html=True)
        st.code('''
    # Sample code for model usage
    def load_model(model_path):
        # Your code to load the model
        pass

    def test_model(data_path):
        # Your code to test the model
        pass
        ''')

    # st.progress(50)
    # st.write("<div class='big-font japanese-style'>Model variant1: with optimize quantization acc: 90%, latency:15ms</div>", unsafe_allow_html=True)
    # st.write("<div class='big-font japanese-style'>Model variant2: with onnx simplify acc: 98%, latency:17ms</div>", unsafe_allow_html=True)
    # st.write("<div class='big-font japanese-style'>Model variant3: ...... acc: 待填充, latency:待填充</div>", unsafe_allow_html=True)

    # Download button
    # st.markdown("<div class='download-button'>Download All!</div>", unsafe_allow_html=True)


# 根据用户的选择调整侧边栏和主页面的展示
# （这部分需要您根据具体逻辑来实现）