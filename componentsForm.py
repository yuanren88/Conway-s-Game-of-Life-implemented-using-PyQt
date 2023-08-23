import sys
import json
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QGridLayout, QMessageBox

class ComponentsDialog(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)

    # 读取JSON文件并解析
    with open('CellComponents.json') as file:
      self.data = json.load(file)

    # 创建按钮并连接点击事件
    self.create_buttons()

    # 设置窗体布局为网格布局
    layout = QGridLayout()
    for index, button in enumerate(self.buttons):
      row = index // 3  # 每行3个
      col = index % 3
      layout.addWidget(button, row, col)
    self.setLayout(layout)

    # 用于存储点击按钮的矩阵
    self.clicked_matrix = None

  def create_buttons(self):
    self.buttons = []
    for item in self.data:
      component = item['构件']
      description = item['描述']
      matrix = item['矩阵']

      button = QPushButton(component)
      button.setToolTip(description)
      button.clicked.connect(lambda state, m=matrix: self.on_button_clicked(m))
      self.buttons.append(button)

  def on_button_clicked(self, matrix):
    self.clicked_matrix = matrix
    self.close()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = ComponentsDialog()
  window.show()

  # 在外部窗口调用这个窗口
  result = app.exec_()
  if result == 0:
    clicked_matrix = window.clicked_matrix
    print("点击的矩阵为：", clicked_matrix)

  sys.exit(result)
