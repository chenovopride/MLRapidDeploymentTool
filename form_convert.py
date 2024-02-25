import torch
import torch.onnx
import tensorflow as tf
import tf2onnx
import onnx

# ------
# ↓↓↓↓ to onnx ↓↓↓↓
# ------
# 1 pth to onnx
def pth_to_onnx():
    import torch
import torch.onnx

def convert_pytorch_to_onnx(model, onnx_model_path, input_shape=(1, 3, 224, 224), device='cpu'):
    """
    Convert a PyTorch model to ONNX format.
    # Example usage:
    # model = MyPyTorchModel()  # Assuming you have a PyTorch model defined
    # convert_pytorch_to_onnx(model, '/path/to/save/model.onnx')

    Parameters:
    - model: The PyTorch model to convert. This can be a model loaded with torch.load or defined in code.
    - onnx_model_path: Path where the ONNX model will be saved.
    - input_shape: The shape of the input tensor to the model. Default is (1, 3, 224, 224) for a single image with 3 channels (e.g., RGB) and 224x224 pixels.
    - device: The device to run the model on ('cpu' or 'cuda').

    Returns:
    - None
    """
    # Set the model to evaluation mode
    model.eval()

    # Move the model to the specified device
    model.to(device)

    # Create a dummy input tensor with the specified shape
    dummy_input = torch.randn(*input_shape, device=device)

    # Export the model to ONNX format
    torch.onnx.export(model, dummy_input, onnx_model_path, export_params=True, opset_version=11,
                      do_constant_folding=True, input_names=['input'], output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})

    print(f"Model successfully converted to ONNX and saved at {onnx_model_path}")


    model = Demucs(sample_rate=44100,hidden=64,chin=2,chout=2,depth=4)
    PATH = '/root/eff_model_v1/model_c2_dep4_db18_effv2_epo50.pth'
    model.load_state_dict(torch.load(PATH))
    model.eval()

    input_names = ["input_0"]
    output_names = ["output_0"]

    x=torch.randn((1,2,441), dtype=torch.float32)

    # torch.onnx.export(model,(x),'model_c2l441_0128.onnx',input_names=input_names,output_names=output_names, opset_version=11,
    #   dynamic_axes={'input_0':[0],'output_0':[0]})
    torch.onnx.export(model,x,'/root/eff_model_v1_onnx/model_c2_dep4_db18_effv2_epo50_new.onnx',input_names=input_names,output_names=output_names, opset_version=11 )

# 2 tf to onnx



def convert_tf_to_onnx(model_path, onnx_model_path, model_type='saved_model', input_signature=None):
    """
    Convert a TensorFlow model to an ONNX model.
    # Example usage:
    # convert_tf_to_onnx('/path/to/tf_model', '/path/to/save/onnx_model.onnx', model_type='saved_model')

    Parameters:
    - model_path: Path to the TensorFlow model. This can be a saved model directory, a .pb file, or a .h5 file.
    - onnx_model_path: Path where the ONNX model will be saved.
    - model_type: Type of the TensorFlow model ('saved_model', 'pb', or 'keras').
    - input_signature: Only needed for 'pb' model type. A list describing the model input, e.g., [tf.TensorSpec([None, 224, 224, 3], tf.float32, name='input')].

    Returns:
    - None
    """
    if model_type == 'saved_model':
        # Convert TensorFlow SavedModel to ONNX
        spec = tf2onnx.convert.from_saved_model(model_path, output_path=onnx_model_path)
    elif model_type == 'pb':
        # Convert TensorFlow .pb model to ONNX
        if input_signature is None:
            raise ValueError("input_signature is required for 'pb' model type")
        spec = tf2onnx.convert.from_graph_def(model_path, input_signature, output_path=onnx_model_path)
    elif model_type == 'keras':
        # Load the Keras model
        keras_model = tf.keras.models.load_model(model_path)
        # Convert Keras model to ONNX
        spec = tf2onnx.convert.from_keras(keras_model, output_path=onnx_model_path)
    else:
        raise ValueError("Unsupported model_type. Use 'saved_model', 'pb', or 'keras'.")

    print("Model conversion complete. ONNX model saved at:", onnx_model_path)


# ------
# ↓↓↓↓ onnx to others ↓↓↓↓
# ------

# onnx to mnn

# onnx to trt