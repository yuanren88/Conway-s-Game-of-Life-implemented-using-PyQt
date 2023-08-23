from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGraphicsView, QGraphicsScene, QMenuBar, QAction, QToolBar, QPushButton, QStatusBar, QLabel, QWidget, QDialog, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QColorDialog
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import numpy as np

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("参数设置")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        # 长度设置
        length_label = QLabel("地图长度:")
        self.length_edit = QLineEdit()
        length_layout = QHBoxLayout()
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_edit)
        layout.addLayout(length_layout)

        # 宽度设置
        width_label = QLabel("地图宽度:")
        self.width_edit = QLineEdit()
        width_layout = QHBoxLayout()
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_edit)
        layout.addLayout(width_layout)

        # 细胞大小设置
        cell_size_label = QLabel("元胞大小:")
        self.cell_size_edit = QLineEdit()
        cell_size_layout = QHBoxLayout()
        cell_size_layout.addWidget(cell_size_label)
        cell_size_layout.addWidget(self.cell_size_edit)
        layout.addLayout(cell_size_layout)


        # 元胞颜色设置
        color_label = QLabel("元胞颜色:")
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.select_color)
        color_layout = QHBoxLayout()
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        layout.addLayout(color_layout)

        # 鼠标调整设置
        mouse_label = QLabel("鼠标调整:")
        self.mouse_edit = QLineEdit()
        mouse_layout = QHBoxLayout()
        mouse_layout.addWidget(mouse_label)
        mouse_layout.addWidget(self.mouse_edit)
        layout.addLayout(mouse_layout)

        # 时钟时间设置
        clock_label = QLabel("时钟时间:")
        self.clock_edit = QLineEdit()
        clock_layout = QHBoxLayout()
        clock_layout.addWidget(clock_label)
        clock_layout.addWidget(self.clock_edit)
        layout.addLayout(clock_layout)

        # 确定和取消按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_color(self):
        self.mycolor = QColorDialog.getColor()
        if self.mycolor.isValid():
            self.color_button.setStyleSheet(f"background-color: {self.mycolor.name()};")

if __name__ == '__main__':
    app = QApplication([])
    dialog = SettingsDialog()
    dialog.show()
    app.exec_()
