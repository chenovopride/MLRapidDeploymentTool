# import torch
# import torch.onnx
# import tensorflow as tf
# import tf2onnx
import onnx
from onnx_tf.backend import prepare
# import tensorflow_probability
from pathlib import Path
import os
import subprocess
import coremltools as ct
# import onnx_coreml


'''
本页代码提供onnx模型转换功能。支持的目标格式有：
- 更适合移动端使用的：mnn、ncnn、tnn 
- 更适合英伟达显卡使用的：tensorRT(.trt)
- 通用格式：onnx格式，不用转换
- 更适合嵌入式、微处理器平台的：tflite (需要进一步转换为c数组并编译到目标平台的程序中)
- 一般用于训练的：tensorflow saved_model 格式（文件夹形式）

'''

# # ------
# # ↓↓↓↓ to onnx ↓↓↓↓
# # ------
# # 1 pth to onnx
# def pth_to_onnx():
#     import torch
# import torch.onnx

# def convert_pytorch_to_onnx(model, onnx_model_path, input_shape=(1, 3, 224, 224), device='cpu'):
#     """
#     Convert a PyTorch model to ONNX format.
#     # Example usage:
#     # model = MyPyTorchModel()  # Assuming you have a PyTorch model defined
#     # convert_pytorch_to_onnx(model, '/path/to/save/model.onnx')

#     Parameters:
#     - model: The PyTorch model to convert. This can be a model loaded with torch.load or defined in code.
#     - onnx_model_path: Path where the ONNX model will be saved.
#     - input_shape: The shape of the input tensor to the model. Default is (1, 3, 224, 224) for a single image with 3 channels (e.g., RGB) and 224x224 pixels.
#     - device: The device to run the model on ('cpu' or 'cuda').

#     Returns:
#     - None
#     """
#     # Set the model to evaluation mode
#     model.eval()

#     # Move the model to the specified device
#     model.to(device)

#     # Create a dummy input tensor with the specified shape
#     dummy_input = torch.randn(*input_shape, device=device)

#     # Export the model to ONNX format
#     torch.onnx.export(model, dummy_input, onnx_model_path, export_params=True, opset_version=11,
#                       do_constant_folding=True, input_names=['input'], output_names=['output'],
#                       dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})

#     print(f"Model successfully converted to ONNX and saved at {onnx_model_path}")


#     model = Demucs(sample_rate=44100,hidden=64,chin=2,chout=2,depth=4)
#     PATH = '/root/eff_model_v1/model_c2_dep4_db18_effv2_epo50.pth'
#     model.load_state_dict(torch.load(PATH))
#     model.eval()

#     input_names = ["input_0"]
#     output_names = ["output_0"]

#     x=torch.randn((1,2,441), dtype=torch.float32)

#     # torch.onnx.export(model,(x),'model_c2l441_0128.onnx',input_names=input_names,output_names=output_names, opset_version=11,
#     #   dynamic_axes={'input_0':[0],'output_0':[0]})
#     torch.onnx.export(model,x,'/root/eff_model_v1_onnx/model_c2_dep4_db18_effv2_epo50_new.onnx',input_names=input_names,output_names=output_names, opset_version=11 )

# # 2 tf to onnx



# def convert_tf_to_onnx(model_path, onnx_model_path, model_type='saved_model', input_signature=None):
#     """
#     Convert a TensorFlow model to an ONNX model.
#     # Example usage:
#     # convert_tf_to_onnx('/path/to/tf_model', '/path/to/save/onnx_model.onnx', model_type='saved_model')

#     Parameters:
#     - model_path: Path to the TensorFlow model. This can be a saved model directory, a .pb file, or a .h5 file.
#     - onnx_model_path: Path where the ONNX model will be saved.
#     - model_type: Type of the TensorFlow model ('saved_model', 'pb', or 'keras').
#     - input_signature: Only needed for 'pb' model type. A list describing the model input, e.g., [tf.TensorSpec([None, 224, 224, 3], tf.float32, name='input')].

#     Returns:
#     - None
#     """
#     if model_type == 'saved_model':
#         # Convert TensorFlow SavedModel to ONNX
#         spec = tf2onnx.convert.from_saved_model(model_path, output_path=onnx_model_path)
#     elif model_type == 'pb':
#         # Convert TensorFlow .pb model to ONNX
#         if input_signature is None:
#             raise ValueError("input_signature is required for 'pb' model type")
#         spec = tf2onnx.convert.from_graph_def(model_path, input_signature, output_path=onnx_model_path)
#     elif model_type == 'keras':
#         # Load the Keras model
#         keras_model = tf.keras.models.load_model(model_path)
#         # Convert Keras model to ONNX
#         spec = tf2onnx.convert.from_keras(keras_model, output_path=onnx_model_path)
#     else:
#         raise ValueError("Unsupported model_type. Use 'saved_model', 'pb', or 'keras'.")

#     print("Model conversion complete. ONNX model saved at:", onnx_model_path)


# ------
# ↓↓↓↓ onnx to others ↓↓↓↓
# ------

# onnx to mnn
def onnx_to_mnn(onnx_model_path, mnn_model_path=None, convert_model_path = "converted_models"):

    """
    Convert onnx model to mnn model

    Parameters:
    - onnx_model_path: Path to the input ONNX model.
    - mnn_model_path: Path where the optimized ONNX model will be saved.
    - convert_model_path: Default path for converted model.
    """

    if mnn_model_path == None:
        mnn_model_path_name = Path(onnx_model_path).name[0:-5] +".mnn"
        # mnn_model_path = convert_model_path + mnn_model_path_name
        mnn_model_path = os.path.join(os.getcwd(), convert_model_path, mnn_model_path_name)
        print("onnx_model_path:", onnx_model_path)
        print("mnn_model_path:", mnn_model_path)
    else:
        mnn_model_path = mnn_model_path

    command = 'MNNConvert'
    # 将命令的各个部分组合成一个列表
    cmd = [command, "-f","ONNX", "--modelFile", onnx_model_path,"--MNNModel", mnn_model_path]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        # print(result.stdout)
        print("MNN model converted successfully!")
        return mnn_model_path
    else:
        print("Failed to convert the mnn model.")
        print("Error message:", result.stdout)
        print("Error message:", result.stderr)
        return None

# onnx to trt

def onnx_to_tflite(onnx_model_path, tflite_model_path=None, convert_model_path = "converted_models"):

    tf_model_path_name = Path(onnx_model_path).name[0:-5]+"_tf"
    tf_model_path = os.path.join(os.getcwd(), convert_model_path, tf_model_path_name)

    if tflite_model_path == None:
        tflite_model_path_name = Path(onnx_model_path).name[0:-5] +".tflite"
        tflite_model_path = os.path.join(os.getcwd(), convert_model_path, tflite_model_path_name)
        print("onnx_model_path:", onnx_model_path)
        print("tflite_model_path:", tflite_model_path)
    else:
        tflite_model_path = tflite_model_path

    onnx_model = onnx.load(onnx_model_path)

    # 使用onnx-tf转换ONNX模型为TensorFlow模型
    tf_rep = prepare(onnx_model)
    tf_rep.export_graph(tf_model_path)

    # 转换为tflite模型
    converter = tf.lite.TFLiteConverter.from_saved_model(tf_model_path)
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, 
                                            # ↑ 这个参数指定使用 TensorFlow Lite 的内置操作集合。内置操作是专门为 TensorFlow Lite 优化过的，可以在不同的平台上提供高效的性能。
                                            # ↓ 这个参数指定允许使用 TensorFlow 操作集合中的操作，这些操作在 TensorFlow Lite 中没有专门的内置实现。
                                            tf.lite.OpsSet.SELECT_TF_OPS]
    # converter._experimental_lower_tensor_list_ops = False
    tflite_model = converter.convert()

    # 保存TFLite模型
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)

    return tflite_model_path

def onnx_to_tensorflow(onnx_model_path, tf_model_path=None, convert_model_path = "converted_models"):

    if tf_model_path == None:
        tf_model_path_name = Path(onnx_model_path).name[0:-5] +"_tf"
        tf_model_path = os.path.join(os.getcwd(), convert_model_path, tf_model_path_name)
        print("onnx_model_path:", onnx_model_path)
        print("tf_model_path:", tf_model_path)
    else:
        tf_model_path = tf_model_path

    onnx_model = onnx.load(onnx_model_path)

    # 使用onnx-tf转换ONNX模型为TensorFlow模型
    tf_rep = prepare(onnx_model)
    tf_rep.export_graph(tf_model_path)

    return tf_model_path

def onnx_to_coreml(onnx_model_path, coreml_model_path=None, convert_model_path = "converted_models"):
    
    '''
    有问题，会转换失败
    '''
    # model_coreml = ct.converters.onnx.convert(model=onnx_model_path)

    if coreml_model_path == None:
        coreml_model_path_name = Path(onnx_model_path).name[0:-5] +".mlmodel"
        coreml_model_path = os.path.join(os.getcwd(), convert_model_path, coreml_model_path_name)
        print("onnx_model_path:", onnx_model_path)
        print("coreml_model_path:", coreml_model_path)

    # 保存CoreML模型
    # coreml_model = onnx_coreml.convert(onnx_model_path)
    # 使用coremltools将ONNX模型转换为CoreML格式
    coreml_model = ct.converters.onnx.convert(model=onnx_model_path)  
    coreml_model.save(coreml_model_path)

    return coreml_model_path

def tf_to_coreml(tf_model_dir, coreml_model_path=None, convert_model_path = "converted_models"):

    '''
    有问题，会转换失败
    '''

    if coreml_model_path == None:
        coreml_model_path_name = Path(tf_model_dir).name +".mlmodel"
        coreml_model_path = os.path.join(os.getcwd(), convert_model_path, coreml_model_path_name)
        print("coreml_model_path:", coreml_model_path)

    # 转换模型
    # 如果你的模型有特定的输入输出格式要求，可能需要在这里指定
    model = ct.convert(
        tf_model_dir,
        source='tensorflow'
    )
    # 保存转换后的 Core ML 模型
    model.save(coreml_model_path)
 
onnx_model_path = r'onnx_models\model_c2_dep4_db18_gun.onnx'
tf_model_path = r'converted_models\model_c2_dep4_db18_gun_tf'

# onnx_to_tflite(onnx_model_path)
# onnx_to_tensorflow(onnx_model_path)
# onnx_to_mnn(onnx_model_path)
# tf_to_coreml(tf_model_path)