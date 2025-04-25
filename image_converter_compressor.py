import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QComboBox, QSpinBox, QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
from PIL import Image

class ImageConverterCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        QIcon_path = os.path.join(os.path.dirname(__file__), 'pic', 'logo128x128.ico')
        self.setWindowIcon(QIcon('app.ico'))

    def initUI(self):
        # 创建布局
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        format_layout = QHBoxLayout()
        quality_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # 设置字体
        font = QFont()
        font.setPointSize(12)

        # 选择图片文件
        self.file_label = QLabel("未选择图片")
        self.file_label.setFont(font)
        self.select_button = QPushButton("选择图片")
        self.select_button.setFont(font)
        self.select_button.clicked.connect(self.select_image)
        input_layout.addWidget(self.file_label)
        input_layout.addWidget(self.select_button)

        # 选择输出格式
        self.format_label = QLabel("输出格式:")
        self.format_label.setFont(font)
        self.format_combobox = QComboBox()
        self.format_combobox.addItems(["JPEG", "PNG", "GIF", "ICO"])
        self.format_combobox.setFont(font)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combobox)

        # 选择压缩质量
        self.quality_label = QLabel("压缩质量 (1-100):")
        self.quality_label.setFont(font)
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(1, 100)
        self.quality_spinbox.setValue(100)  # 默认不压缩
        self.quality_spinbox.setFont(font)
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_spinbox)

        # 转换和压缩按钮
        self.convert_button = QPushButton("转换并压缩")
        self.convert_button.setFont(font)
        self.convert_button.clicked.connect(self.convert_and_compress)
        button_layout.addWidget(self.convert_button)

        # 将布局添加到主布局
        main_layout.addLayout(input_layout)
        main_layout.addLayout(format_layout)
        main_layout.addLayout(quality_layout)
        main_layout.addLayout(button_layout)

        # 设置主布局
        self.setLayout(main_layout)
        self.setWindowTitle('图片转换与压缩')
        self.setGeometry(100, 100, 600, 400)  # 设置较大的默认窗口大小
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QSpinBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)  # 美化界面的样式表
        self.show()

    def select_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.gif)")
        if file_path:
            # 获取文件名
            file_name = os.path.basename(file_path)
            self.file_label.setText(file_name)

    def convert_and_compress(self):
        input_file = self.file_label.text()
        if input_file == "未选择图片":
            return
        output_format = self.format_combobox.currentText().lower()
        quality = self.quality_spinbox.value()
        output_file, _ = QFileDialog.getSaveFileName(self, "保存图片", "", f"{output_format.upper()} 文件 (*.{output_format})")
        if output_file:
            try:
                image = Image.open(input_file)
                if output_format == 'ico':
                    # ICO 格式需要指定尺寸
                    sizes = [(32, 32)]
                    image.save(output_file, format=output_format, sizes=sizes)
                else:
                    image.save(output_file, format=output_format, quality=quality)
                QMessageBox.information(self, "完成", f"图片已转换并压缩为 {output_file}")

                if output_format != 'ico':
                    # 调用系统默认程序打开文件
                    os.startfile(output_file) if os.name == 'nt' else os.system(f'xdg-open {output_file}')
            except Exception as e:
                QMessageBox.critical(self, "错误", f"发生错误: {e}")
                
# The packaging cannot display Chinese characters, otherwise the icon will become the default image
# pyinstaller .\image_converter_compressor.py --onefile -w -F --distpath .\ --name image_converter_compressor --icon=app.ico 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = ImageConverterCompressor()
    sys.exit(app.exec())
    