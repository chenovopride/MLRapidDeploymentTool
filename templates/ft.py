import flet as ft

def main(page: ft.Page):
    page.title = "Model Optimization Interface"

    # 上传模型
    model_upload = ft.FilePicker()
    page.add(model_upload)

    # 上传测试数据
    data_upload = ft.FilePicker()
    page.add(data_upload)

    # 选择输出格式
    output_format = ft.Dropdown(
        label="Select output format",
        options=[ft.DropdownOption("Format 1"), ft.DropdownOption("Format 2")]
    )
    page.add(output_format)

    # 选择优先级
    priority = ft.TextField(label="Select priority")
    page.add(priority)

    # 生成按钮
    generate_btn = ft.ElevatedButton(text="Generate!", on_click=generate_model)
    page.add(generate_btn)

    # 添加其他组件和样式...

def generate_model(e):
    # 生成模型逻辑
    pass

ft.app(target=main)
