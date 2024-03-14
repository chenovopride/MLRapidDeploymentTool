# from MobileNetV2 import mobilenet_v2

# net = mobilenet_v2(pretrained=True)
import numpy as np 

shape = (2,1000)
# 星号（*）用在参数前面表示"解包"操作。当你在函数调用中使用*时，它会将序列（例如列表、元组）中的每个元素都作为独立的参数传递给函数
x = np.random.rand(*shape)
print(x)