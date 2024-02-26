from onnxsim import simplify
import onnx
# import onnxmltools
# from onnxmltools.utils.float16_converter import convert_float_to_float16
import onnxruntime as ort
import numpy as np
import time
from onnxruntime.quantization import QuantType, quantize_dynamic
import subprocess

'''
本页代码提供onnx模型有效性验证、多种onnx模型计算图优化函数、模型推理时间测量的功能
'''

def onnx_verify(onnx_model_path):

    '''
    model verification 
    '''

    model = onnx.load(onnx_model_path)
    try:
        onnx.checker.check_model(model)
        print("model verification success!")
        return True
    except Exception as e:
        print(f"ONNX model error: {e}")
        return False

def onnx_simple(onnx_model_path, output_path=None):

    '''
    Simplify the ONNX model. Simplification may include removing unnecessary operations from the model and optimizing the graph structure
    
    Parameters:
    - onnx_model_path: 'path_to_your_model.onnx' 
    - output_model_path: Path where the optimized ONNX model will be saved.
    '''
    onnx_model = onnx.load(onnx_model_path)
    model_simp, check = simplify(onnx_model)
    assert check, "Simplified ONNX model could not be validated. Model simplification operation failed."
    if output_path == None:
        output_path = onnx_model_path[0:-5]+"_simp.onnx"
    else:
        output_path = output_path
    onnx.save(model_simp, output_path)
    print('finished exporting simplified onnx!')

def optimize_onnx_model(input_model_path, output_model_path=None):
    """
    Optimize an ONNX model using the onnxoptimizer.

    Parameters:
    - input_model_path: Path to the input ONNX model.
    - output_model_path: Path where the optimized ONNX model will be saved.
    """
    if output_model_path == None:
        output_model_path = input_model_path[0:-5]+"_opt.onnx"
    else:
        output_model_path = output_model_path

    command = ["python", "-m", "onnxoptimizer", input_model_path, output_model_path]
    # 确保了输出以文本形式
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Model optimized successfully!")
    else:
        print("Failed to optimize the model.")
        print("Error message:", result.stderr)

def onnx_to_fp16(output_path):

    out_model = convert_float_to_float16(onnx_model)
    onnxmltools.utils.save_model(out_model, output_path)
    
# output_path = '/root/onnx_optSimple_model_0128_dep5_441.onnx'
# onnx_simple(output_path)


def onnx_quantize_dynamic(onnx_model_path, quant_type = "int8", output_path=None):

    """
    Quantize an ONNX model dynamically and save the quantized model to a specified path.

    Parameters:
    - onnx_model_path: Path to the input ONNX model.
    - quant_type: Type of quantization to apply ('uint8' or 'int8'). Default is 'int8'.
    - output_path: Path where the quantized ONNX model will be saved. If None, the quantized model will be saved
                   next to the original model with a "_quant" suffix.

    Returns:
    - None
    """
        
    if quant_type == "int8":
        qtype = QuantType.QInt8
    elif quant_type == "uint8":
        qtype = QuantType.QUInt8
    else:
        raise ValueError("Unsupported quantization type. Please choose 'uint8' or 'int8'.")

    if output_path == None:
        output_path = onnx_model_path[0:-5] + "_quant_"+ quant_type + ".onnx"
    else:
        output_path = output_path

    print("Start quantization...")
    # quantize_dynamic (
    #     model_input=onnx_model_path, # 输入模型
    #     model_output=model_quant_dynamic, # 输出模型
    #     weight_type=qtype, # 参数类型 Int8 / UInt8
    #     optimize_model=True # 是否优化模型这个参数新版本没了
    # )

    quantize_dynamic (
        model_input=onnx_model_path, # 输入模型
        model_output=output_path, # 输出模型
        weight_type=qtype,
        optimize_model=True
    )
    print(f"Dynamic quantization success! Model saved to {output_path}")


def onnx_infer(onnx_model_path, input_data_shape, input_data = None):
    # 浓缩型写法：
    # ort_session = ort.InferenceSession(onnx_model_path)
    # outputs = ort_session.run(None,{'input_0':block.astype('float32')})
    """
    Parameters:
    - onnx_model_path: 'path_to_your_model.onnx' 
    - input_data_shape: tuple, eg. (2,1000)
    - input_data: alterntive, .npy 

    Returns:
    """
    try:
        session = ort.InferenceSession(onnx_model_path)
    except Exception as e:
        print(f"Error loading the ONNX model: {e}")
        return None
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    if input_data is None:
        # 星号（*）用在参数前面表示"解包"操作。
        # 当你在函数调用中使用*时，它会将序列（例如列表、元组）中的每个元素都作为独立的参数传递给函数
        input_data = np.random.randn(*input_data_shape).astype(np.float32)
    else:
        input_data = input_data.astype(np.float32)

    inputs = {input_name: input_data}

    try:
        outputs = session.run([output_name], inputs)
        return outputs
    except Exception as e:
        print(f"Error during inference: {e}")
        return None



def infer_mean_time_measurement(func, loop_cnt=20):
    """
    Measure the average execution time of a function over a specified number of loops, in milliseconds.

    Parameters:
    - func: The function to measure. This function should take no arguments.
    - loop_cnt: The number of times to execute the function for averaging. Default is 20.

    Returns:
    - The average execution time of the function over the specified number of loops, in milliseconds.
    """
    total_time = 0  # 用于累加每次执行func的时间

    for _ in range(loop_cnt):
        start_time = time.time() * 1000  # 记录函数执行前的时间，并转换为毫秒
        func()  # 执行函数
        end_time = time.time() * 1000  # 记录函数执行后的时间，并转换为毫秒
        total_time += (end_time - start_time)  # 累加函数执行耗时

    average_time = total_time / loop_cnt  # 计算平均耗时
    
    print(f"The average execution time of the infer_function is: {average_time} milliseconds")
    return average_time





onnx_model_path = r'onnx_models\model_c2_dep4_db18_gun.onnx'


optimize_onnx_model(onnx_model_path)
# onnx_verify(onnx_model_path) # ok
# onnx_simple(onnx_model_path) # ok
# average_time = infer_mean_time_measurement(onnx_infer, loop_cnt=20) #ok
# onnx_quantize_dynamic(onnx_model_path, quant_type = "uint8") #ok

