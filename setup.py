#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='xdeployai',
    version='0.0.1',
    description='快速模型部署工具',
    long_description='项目的长描述',
    author='chenovopride',
    author_email='1832292582@qq.com',
    url='https://github.com/chenovopride/MLRapidDeploymentTool',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'numpy',
        'onnx',
        'onnxsim',
        'onnxruntime',
        'tensorflow~=2.15.0',
        'tf2onnx',
        'tf_keras',
        'onnx_tf',
        'tensorflow_probability~=0.23.0',
        'netron',
        'coremltools',
    ],
    python_requires='>=3.8',
    # 其他参数...
    entry_points={
        'console_scripts': [
            'tst = XdeployAI:test',
            'run = XdeployAI.run:webdemo',
            'xdeployrun = XdeployAI:run_deploy'
        ]
    }
)