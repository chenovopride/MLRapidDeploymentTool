import streamlit as st
import subprocess
import webbrowser
from XdeployAI.varient_generate_select import *
import time

def display_main_info():
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

def model_variant_generate(input_model_path, out_format = "onnx", quant = False, optimize = False, advance = False, optimization_priority = None, output_model_dir = "converted_models"):

    st.session_state.generate = True

    if (out_format == "onnx") and (quant == False) and (optimize == False) and  (advance == False):
        opt_model_path = input_model_path
        print("用户没有选择任何转换和优化操作！！")
    else:
        opt_model_path = model_variant_generate_backend(input_model_path, out_format, quant, optimize, advance, optimization_priority, output_model_dir)
    
    if opt_model_path != None:
        # 转换成功
        print("转换操作成功")
        st.session_state.out_model_path = opt_model_path

        with st.spinner('Model generation progress...'):
            time.sleep(3)
        # model_variant_generate_state(input_model_path, out_format, quant, optimize, output_model_dir)
    else:
        print("转换操作失败")

def display_the_sidebar():

    with st.sidebar:

        # 侧边栏 - 模型上传
        st.header('操作栏')
        uploaded_model = st.file_uploader("上传您的.onnx模型", type=["onnx"])
        uploaded_model_path = None

        # 如果上传了model
        if uploaded_model is not None:
            if not os.path.exists('onnx_uploads'):
                os.makedirs('onnx_uploads', exist_ok=True)

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
        model_format = st.sidebar.selectbox('模型转换格式选择', ['onnx', 'mnn', 'tflite', 'tf', 'coreML','...'])
        # if model_format == 'onnx':
        #     st.sidebar.info('模型将继续保持onnx格式，仅进行您选择的优化')
        st.caption("选择您想要转换的模型格式，如果选择onnx格式，将不进行格式转换。", unsafe_allow_html=True)
        quantize_model = st.sidebar.checkbox('是否需要模型量化')
        optimize_model = st.sidebar.checkbox('是否需要经过简单优化')

        # 工具提示
        if quantize_model:
            st.sidebar.info('模型量化会减小模型体积但是会损失精度')
        if optimize_model:
            st.sidebar.info('简单优化仅消除冗余操作，不影响精度')

        st.markdown("---")

        advance = False 
        optimization_priority = None
        # 侧边栏 - 高级选项
        if st.sidebar.checkbox('高级选项'):
            st.caption("选择后，软件可自动帮您生成所有可能的优化结果，并自动测试推理延迟，返回最优模型。", unsafe_allow_html=True)
            st.sidebar.text_input('填写模型输入尺寸')
            optimization_priority = st.sidebar.radio(
                '更注重准确性还是延迟', ['accuracy', 'lantency']
            )
            advance = True
        generate_button = st.button('Generate!', type="primary")
        if generate_button:
            model_variant_generate(uploaded_model_path, model_format, quantize_model, optimize_model, advance, optimization_priority)
        # if st.button('Generate!', type="primary",
        #              on_click = model_variant_generate,
        #              args=(uploaded_model_path, model_format, quantize_model, optimize_model, advance, optimization_priority, )
        #              ):
            if uploaded_model_path == None:
                st.sidebar.info('您还未选择模型！')
            else:
                st.sidebar.success("Model generation started! May need sometime...")


def display_progress_info(model_path = None):

    if model_path == None:
        opt_model_path = "onnx_models\model_c2_dep4_db18_gun_opt.onnx"
    else:
        opt_model_path = model_path

    see_opt_model_button = st.button('查看生成的模型结构', key = "see_opt_model")
    # download_clicked_button = st.button('下载生成的模型', key = "download_clicked")

    if see_opt_model_button:
        visualize_model(opt_model_path)
        print("st.session_state.see_opt_model:", st.session_state.see_opt_model)

    print("优化后的模型：", opt_model_path)
    with open(opt_model_path, "rb") as file:
        btn = st.download_button(
                label="下载生成的模型",
                data=file,
                file_name="your_model.onnx",
                mime="application/octet-stream"
            )
    # TODO : 这里每次点击都会显示一遍
    if btn:
        print("用户正在下载优化后的模型：", opt_model_path)
        print("-----模型下载完毕-----")

    
def download_generated_model(model_path):
    file_path = model_path
    with open(file_path, "rb") as file:
        btn = st.download_button(
                label="Download the optimized model",
                data=file,
                file_name="your_model.onnx",
                mime="application/octet-stream",
                on_click=lambda: setattr(st.session_state, 'download_clicked', True)
            )
    # if st.session_state.download_clicked:
    #     # 显示下载后的信息
    #     st.success('Model downloaded successfully!')
    # else:
    #     print("chucuol!! ")


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

        


def main():
    if 'generate' not in st.session_state:
        st.session_state.generate = False
    if 'download_clicked' not in st.session_state:
        st.session_state.download_clicked = False
    if 'see_opt_model' not in st.session_state:
        st.session_state.see_opt_model = False
    if 'see_ori_model' not in st.session_state:
        st.session_state.see_ori_model = False
    if 'out_model_path' not in st.session_state:
        st.session_state.out_model_path = None

    display_the_sidebar()
    display_main_info()

    if ('generate' in st.session_state) and (st.session_state.generate) == True:
        st.success('模型转换：<br>模型优化：<br>已全部成功！')
        display_progress_info(st.session_state.out_model_path)
        display_sample_code()
        
if __name__ == '__main__':
    main()