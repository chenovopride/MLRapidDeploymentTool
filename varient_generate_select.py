# from form_convert import *
from onnx_optimize import *

def model_variant_generate_backend(input_model_path, out_format = "onnx", quant = False, optimize = False, output_model_dir = "converted_models"):
    print("---hello---")
    print(input_model_path, out_format, quant, optimize)

    # 先quant 和 opt 之后再转换模型

    # onnx_model_path = r'onnx_models\model_c2_dep4_db18_gun.onnx'

    # optimize_onnx_model(onnx_model_path)
    # onnx_verify(onnx_model_path) # ok
    # onnx_simple(onnx_model_path) # ok
    # average_time = infer_mean_time_measurement(onnx_infer, loop_cnt=20) #ok
    # onnx_quantize_dynamic(onnx_model_path, quant_type = "uint8") #ok


