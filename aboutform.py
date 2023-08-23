from PyQt5.QtWidgets import QApplication,  QVBoxLayout, QGraphicsView, QGraphicsScene, QMenuBar, QAction, QToolBar, QPushButton, QStatusBar, QLabel, QWidget, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("关于")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        # 添加程序图标
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("life.png"))
        layout.addWidget(icon_label)

        # 添加作者信息
        author_label = QLabel("作者：猿人")
        layout.addWidget(author_label)

        # 添加联系群
        group_label = QLabel("联系群：群号123456")
        layout.addWidget(group_label)

        # 添加作者邮件（超链接）
        email_label = QLabel()
        email_label.setText('<a href="mailto:32268930@qq.com">32268930@qq.com</a>')
        email_label.setOpenExternalLinks(True)
        layout.addWidget(email_label)

        # 添加退出按钮
        exit_btn = QPushButton("退出")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(layout)

