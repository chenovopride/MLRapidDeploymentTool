# from form_convert import *
from .onnx_optimize import *
from .form_convert import *

def optimize_and_evaluate():
    pass 

def fast_optimization(input_model_path, out_format = "onnx", quant = False, optimize = False):
    # pass 
    # 1 optimize
    simp_model_path = onnx_simple(input_model_path, output_path=None)
    temp_model_path = simp_model_path

    # 2 qunat (if selected)
    if quant == True:
        quant_model_path = onnx_quantize_dynamic(simp_model_path, quant_type = "int8")
        temp_model_path = quant_model_path
    
    if out_format != "onnx":
        out_model_path = model_convert(out_format, temp_model_path)
    else:
        out_model_path = temp_model_path

    return out_model_path

def model_convert(out_format, onnx_model_path):

    out_model_path = None

    if out_format == "mnn":
        out_model_path = onnx_to_mnn(onnx_model_path)
    elif out_format == "tflite":
        out_model_path = onnx_to_tflite(onnx_model_path)
    elif out_format == "tf":
        out_model_path = onnx_to_tensorflow(onnx_model_path)
    elif out_format == "coreML":
        # pass
        out_model_path = None
    else:
        out_model_path = None

    return out_model_path

def model_variant_generate_backend(input_model_path, out_format = "onnx", quant = False, optimize = False, advance = False, optimization_priority = None, output_model_dir = "converted_models"):

    print("---hello---")
    print(input_model_path, out_format, quant, optimize, advance, optimization_priority)

    output_path = None
    
    if advance == False:
        if optimize == True:
            output_path = fast_optimization(input_model_path, out_format, quant, optimize)
        else:
            # TODO 这里忘记添加量化了？
            print("用户没有选择任何转换和优化操作！！")
            output_path = input_model_path
    else:
        output_path = optimize_and_evaluate(input_model_path, out_format, quant, optimize, optimization_priority)

    return output_path

    # model_convert()


    # onnx_model_path = r'onnx_models\model_c2_dep4_db18_gun.onnx'

    # optimize_onnx_model(onnx_model_path)
    # onnx_verify(onnx_model_path) # ok
    # onnx_simple(onnx_model_path) # ok
    # average_time = infer_mean_time_measurement(onnx_infer, loop_cnt=20) #ok
    # onnx_quantize_dynamic(onnx_model_path, quant_type = "uint8") #ok


