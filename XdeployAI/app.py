from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # 设置上传文件夹路径
app.config['ALLOWED_EXTENSIONS'] = {'onnx'}  # 允许上传的文件类型
app.secret_key = 'super secret key'  # 设置Flask的密钥，用于维护会话等

# 确保上传的是允许的文件类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件部分
    if 'model' not in request.files or 'test_data' not in request.files:
        flash('No file part')
        return redirect(request.url)
    model_file = request.files['model']
    test_file = request.files['test_data']
    # 如果用户没有选择文件，浏览器也会提交一个空的部分没有文件名
    if model_file.filename == '' or test_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if model_file and allowed_file(model_file.filename):
        model_filename = secure_filename(model_file.filename)
        test_filename = secure_filename(test_file.filename)
        model_file.save(os.path.join(app.config['UPLOAD_FOLDER'], model_filename))
        test_file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_filename))
        # 这里可以添加模型转换和优化的代码
        # 模拟一些处理时间
        time.sleep(2)
        return redirect(url_for('results'))

@app.route('/results')
def results():
    # 在真实应用中，这里应该返回转换和优化后的结果
    return render_template('results.html')

@app.route('/download/<filename>')
def download_file(filename):
    # 安全地发送存储在uploads文件夹的文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # 确保文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
