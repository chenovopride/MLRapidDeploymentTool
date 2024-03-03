import streamlit as st

def display_the_sidebar():
    # 侧边栏 - 模型上传
    st.header('Side action bar')
    uploaded_model = st.file_uploader("Upload your onnx model", type=["onnx"])
    # st.sidebar.header('侧边操作栏')
    # uploaded_model = st.sidebar.file_uploader('模型上传框，上传您的模型')

    # 侧边栏 - 基础选项
    st.sidebar.subheader('基础选项')
    model_format = st.sidebar.selectbox('模型转换格式选择', ['mnn', 'trt', 'ncnn', '...'])
    quantize_model = st.sidebar.checkbox('是否需要模型量化')
    optimize_model = st.sidebar.checkbox('是否需要经过简单优化')

    # 工具提示
    if quantize_model:
        st.sidebar.info('模型量化会减小模型体积但是会损失精度')
    if optimize_model:
        st.sidebar.info('简单优化仅消除冗余操作，不影响精度')

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