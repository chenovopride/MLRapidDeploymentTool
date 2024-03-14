import subprocess
import os 
# def webdemo():
#     # 获取xdeployai包的目录
#     package_dir = os.path.dirname(__file__)  # __file__ 是当前文件(run.py)的路径
#     # 改变工作目录
#     os.chdir(package_dir)

#     print("os.getcwd(): ",os.getcwd())
#     # subprocess.run(["streamlit", "run", "st_onnx_cn.py"], check=True)
#     subprocess.run(["python ", "-m","wrapper","run", "st_onnx_cn.py"], check=True)

def webdemo():
    # 获取xdeployai包的目录
    package_dir = os.path.dirname(__file__)  # __file__ 是当前文件(run.py)的路径
    # 改变工作目录
    os.chdir(package_dir)

    print("os.getcwd(): ",os.getcwd())
    subprocess.run(["streamlit", "run", "st_onnx_cn.py"], check=True)