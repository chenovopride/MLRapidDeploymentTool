# import streamlit as st

# # 定义一个函数来设置页面的样式
# def set_page_style(choice):
#     if choice == "经验丰富的ML工程师":
#         st.markdown("""
#             <style>
#             /* 添加针对经验丰富的ML工程师的自定义样式 */
#             </style>
#         """, unsafe_allow_html=True)
#         # 可以在这里添加更多的页面元素和布局
#     elif choice == "普通的开发工程师":
#         st.markdown("""
#             <style>
#             /* 添加针对普通的开发工程师的自定义样式 */
#             </style>
#         """, unsafe_allow_html=True)
#         # 可以在这里添加更多的页面元素和布局

# # 在session_state中初始化一个key来存储用户的选择
# if 'choice' not in st.session_state:
#     st.session_state['choice'] = None

# # 用radio按钮让用户选择角色
# role = st.radio("请选择您的角色：", ("经验丰富的ML工程师", "普通的开发工程师"))

# # 检测选择变化并存储在session_state中
# if role:
#     st.session_state['choice'] = role

# # 根据当前选择设置页面样式和内容
# if st.session_state['choice']:
#     set_page_style(st.session_state['choice'])

# # 根据选择渲染不同的页面内容
# if st.session_state['choice'] == "经验丰富的ML工程师":
#     st.clean()
#     st.write("欢迎，经验丰富的ML工程师！")
#     # 在这里添加针对经验丰富的ML工程师的页面内容
# elif st.session_state['choice'] == "普通的开发工程师":
#     st.write("欢迎，普通的开发工程师！")
#     # 在这里添加针对普通的开发工程师的页面内容





# import streamlit as st

# st.write("选择模型格式：")
# st.radio("", ["onnx", "caffe", "mxnet"])

# # 使用HTML的title属性创建工具提示
# st.markdown("""
# <span title="onnxsim 能以不同的 onnx optimizer 和优化模型">onnxsim 能以不同的 onnx optimizer 和优化模型</span>
# """, unsafe_allow_html=True)

# # 使用 Streamlit 的 checkboxes 和 markdown 结合 title 属性来创建工具提示
# col1, col2 = st.columns(2)
# with col1:
#     st.checkbox("使用 onnx simplifier 优化模型")
#     st.markdown("""
#     <span title="详细描述 onnx simplifier 如何工作">ℹ️</span>
#     """, unsafe_allow_html=True)

# with col2:
#     st.checkbox("使用 ncnnoptimize 优化模型")
#     st.markdown("""
#     <span title="详细描述 ncnnoptimize 如何工作">ℹ️</span>
#     """, unsafe_allow_html=True)
#     st.markdown("""
#     <span title="详细描述 ncnnoptimize 如何工作">i</span>
#     """, unsafe_allow_html=True)

import streamlit as st

# 侧边栏 - 模型上传
st.sidebar.header('侧边操作栏')
uploaded_model = st.sidebar.file_uploader('模型上传框，上传您的模型')

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

# 主页面 - 日志信息
st.subheader('右边主要栏目：')
st.text('静态说明，显示log信息，文字等')

# 主页面 - 生成按钮
if st.button('Generate'):
    # 模型优化函数执行
    st.write('模型优化函数执行中...')

# 根据用户的选择调整侧边栏和主页面的展示
# （这部分需要您根据具体逻辑来实现）
