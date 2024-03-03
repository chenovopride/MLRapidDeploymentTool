import streamlit as st
import subprocess
import webbrowser

def visualize_model(model_path):

    print("Visualize this model")
    # 在后台运行 Netron 命令
    subprocess.Popen(['netron', model_path, '--host', 'localhost', '--port', '8080'])
    
    # 提示用户即将打开新的网页
    st.write("正在打开Netron...如果没有自动打开，请点击下方的链接。")
    
    # 在新标签页中打开 Netron 界面
    st.markdown("[Open Netron](http://localhost:8080)", unsafe_allow_html=True)

    # 可选：Python自动打开网页（取决于用户的浏览器设置和权限）
    webbrowser.open_new_tab("http://localhost:8080")

def display_the_sidebar():
    
    with st.sidebar:

        # 侧边栏 - 模型上传
        st.header('操作栏')
        uploaded_model = st.file_uploader("上传您的.onnx模型", type=["onnx"])

        # 如果上传了model
        if uploaded_model is not None:
            file_path = "onnx_uploads/temp_" + uploaded_model.name

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
            st.sidebar.text_input('填写模型输入尺寸')
            optimization_priority = st.sidebar.radio(
                '更注重准确性还是延迟', ['准确性', '延迟']
            )

display_the_sidebar()

# 主页面 - 日志信息
st.subheader('右边主要栏目：')
st.text('静态说明，显示log信息，文字等')

# 主页面 - 生成按钮
if st.button('Generate'):
    # 模型优化函数执行
    st.write('模型优化函数执行中...')

# 根据用户的选择调整侧边栏和主页面的展示
# （这部分需要您根据具体逻辑来实现）