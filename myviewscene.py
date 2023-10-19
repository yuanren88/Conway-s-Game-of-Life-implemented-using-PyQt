from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene,QGraphicsRectItem,QMessageBox,QLineEdit
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,QRectF
from PyQt5.QtGui import QWheelEvent,QPen,QClipboard

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout,QHBoxLayout,QVBoxLayout
import componentsForm

class GameView(QGraphicsView):
    def __init__(self,scene):
        super().__init__()
        self.setMouseTracking(True)
        self.scene = scene
        self.setScene(scene)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    def mousePressEvent(self, event):
        self.scene.mousePressEvent(event)

  #   def mouseMoveEvent(self, event): 
  #     self.scene().mouseMoveEvent(event)

    def mouseMoveEvent(self, event):
        self.scene.mouseMoveEvent(event)

    def wheelEvent(self, event):
        self.scene.wheelEvent(event)

    def mouseReleaseEvent(self, event):
        self.scene.mouseReleaseEvent(event)

class GameScene(QGraphicsScene):
    def __init__(self,GameOfLife):
        super().__init__()
        self.GameOfLife=GameOfLife
        self.dragging=False
        self.draged=False
        self.direction=1#表征鼠标控制的gird的朝向方向。
        self.dirstring=['👆', '👉','👇', '👈']
        self.rect_item = None
        self.start_pos = None
        self.left_pressed = False
        self.right_pressed = False
 

    def mousePressEvent(self, event):
        # print(event.button())
        # self.direction=1
        self.right_dragging=False
        if event.button() == Qt.LeftButton:
            self.left_pressed = True
        if event.button() == Qt.RightButton:  
            self.right_pressed = True


        view = self.views()[0]
        pos_in_view = view.mapFromGlobal(event.globalPos())  
        view_pos = view.mapToScene(pos_in_view)
        if event.button() == Qt.LeftButton:
            global_pos = event.globalPos()
            # view_pos = self.GameOfLife.view.mapFromGlobal(global_pos)
            # view_pos = self.GameOfLife.view.mapFromGlobal(global_pos)

            self.dragging = True
            self.drag_start_pos = view_pos  #event.pos()
            # print(self.drag_start_pos)
        elif event.button() ==2:    
            self.GameOfLife.timer.stop()
            self.start_pos = view_pos
            self.rect_item = QGraphicsRectItem()
            self.rect_item.setPen(Qt.red)
            self.addItem(self.rect_item)
        if self.left_pressed and self.right_pressed: 
            self.direction += 1
            if self.direction > 4:
                self.direction = 1  
            self.GameOfLife.status_label4.setText(self.dirstring[self.direction-1])
            self.removeItem(self.rect_item)
            self.rect_item = None


            # print('dir'+str(self.direction))          
        # elif event.button() == Qt.RightButton:
        #     # 左键已经按下的情况下,再点击右键调整方向
        #     if self.dragging:  
        #         self.direction += 1
        #         if self.direction > 4:
        #             self.direction = 1
    # def drawBackground(self, painter, rect):
    #   # 绘制地图边框
    #   painter.setBrush(Qt.black) 
    #   rect = QRectF(0, 0, 
    #         self.GameOfLife.cols * self.GameOfLife.cell_size,
    #         self.GameOfLife.rows * self.GameOfLife.cell_size)
    #   painter.drawRect(rect)

      # for i in range(self.GameOfLife.rows):
      #   for j in range(self.GameOfLife.cols):
      #     brush = QBrush(Qt.white)
      #     painter.fillRect(QRectF(j*self.GameOfLife.cell_size, 
      #                 i*self.GameOfLife.cell_size,
      #                 self.GameOfLife.cell_size,
      #                 self.GameOfLife.cell_size),brush)

    def mouseMoveEvent(self, event):
        # print(event.pos())
        global_pos = event.globalPos()
        # view_pos = self.GameOfLife.view.mapFromGlobal(global_pos)

        view = self.views()[0]
        pos_in_view = view.mapFromGlobal(event.globalPos())  
        view_pos = view.mapToScene(pos_in_view)
        row = int((view_pos.y() ) // self.GameOfLife.cell_size)
        col = int((view_pos.x() ) // self.GameOfLife.cell_size)    
        if self.rect_item :
            endPos = view_pos #self.view.mapToScene(event.pos()) 
            try:
                self.rect_item.setRect(QRectF(self.start_pos, endPos).normalized())
            except:
                pass
            self.right_dragging=True

        self.GameOfLife.status_label2.setText('位置：'+str(col)+' '+str(row))
        if self.dragging:
            delta = view_pos- self.drag_start_pos
            # delta = event.pos() - self.drag_start_pos
            row_offset = int(delta.y() // self.GameOfLife.cell_size)
            col_offset = int(delta.x() // self.GameOfLife.cell_size)
            # print(row_offset, col_offset)
            if row_offset!=0 or col_offset!=0:
                self.GameOfLife.grid =self.GameOfLife.shift_grid(self.GameOfLife.grid, row_offset, col_offset)
                self.drag_start_pos = event.pos()
                self.GameOfLife.draw_grid()
                self.draged=True

    def mouseReleaseEvent(self, event):
        view = self.views()[0]
        pos_in_view = view.mapFromGlobal(event.globalPos())  
        view_pos = view.mapToScene(pos_in_view)        
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.left_pressed = False
            self.right_pressed = False

            if not self.draged:
                row = int((self.drag_start_pos.y() ) // self.GameOfLife.cell_size)
                col = int((self.drag_start_pos.x() ) // self.GameOfLife.cell_size)    
                # self.GameOfLife.add_grid(self.GameOfLife.clicked_matrix, row, col)

                self.GameOfLife.add_grid_with_dir(self.GameOfLife.clicked_matrix, row, col,self.direction)
                self.GameOfLife.draw_grid()
                self.direction=1

        if self.rect_item and self.right_dragging:
            end_pos = view_pos
            srow = int((self.start_pos.y() ) // self.GameOfLife.cell_size)
            scol = int((self.start_pos.x() ) // self.GameOfLife.cell_size)    
            erow = int((end_pos.y() ) // self.GameOfLife.cell_size)
            ecol = int((end_pos.x() ) // self.GameOfLife.cell_size)    

            # print(f"Start pos: {self.start_pos}") 
            # print(f"End pos: {end_pos}")
            # print('startpos',srow,scol)
            # print('endpos',erow,ecol)
            self.removeItem(self.rect_item)
            self.rect_item = None
            # print(self.GameOfLife.grid [srow+1:erow, scol+1:ecol])
            gridstr=str(self.GameOfLife.grid [srow+1:erow, scol+1:ecol])
            # 弹出对话框，显示确定和取消按钮。确定后，将grid存入系统的剪贴板            
            msg_box = QMessageBox()
            msg_box.setWindowTitle("系统警告")
            msg_box.setText("将数据保存到剪贴板?\n"+gridstr)
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Ok)
            ret = msg_box.exec_()
            if ret == QMessageBox.Ok:
                gridstr=self.grid_to_str(self.GameOfLife.grid [srow+1:erow, scol+1:ecol])
                clipboard = QApplication.clipboard()
                clipboard.setText(gridstr)
                self.add_a_cellComponents(gridstr)
        self.draged=False

    def wheelEvent(self, event: QWheelEvent):
        # print(event.angleDelta())
        # if self.hasFocus():
        modifiers = QApplication.keyboardModifiers()
    # modifiers = QApplication.keyboardModifiers()
        # if modifiers == Qt.ControlModifier:
        angle_delta = event.angleDelta().y()
        if angle_delta > 0:
            self.GameOfLife.cell_size += 1
        else:
            self.GameOfLife.cell_size = max(1, self.GameOfLife.cell_size - 1)
        # self.refresh_simulation()
        # print(self.GameOfLife.cell_size)
        self.GameOfLife.draw_grid()
        # else:
        #     event.ignore()
    def draw_lines(self):
        # 绘制表格线
        pen = QPen(Qt.black)
        pen.setWidth(1)
        for i in range(self.GameOfLife.rows+1):
            self.addLine(0, i*self.GameOfLife.cell_size, self.GameOfLife.cols*self.GameOfLife.cell_size, i*self.GameOfLife.cell_size, pen)
        for i in range(self.GameOfLife.cols+1):    
            self.addLine(i*self.GameOfLife.cell_size, 0, i*self.GameOfLife.cell_size, self.GameOfLife.rows*self.GameOfLife.cell_size, pen)

    def add_a_cellComponents(self,grid):
        # cellComponents_dialog = InputDialog(self.GameOfLife)
        # result = cellComponents_dialog.exec_()
        # if result == 0:
        #     name = cellComponents_dialog.name_input.text()
        #     tips = cellComponents_dialog.desc_input.text()
        #     cdata={}
        #     cdata['构件']= name
        #     cdata['描述']= tips
        #     cdata['矩阵']= grid

            # componentsForm.add_components(cdata)
        gouxingstr='{"构件":"'+''+'",\n"描述":"'+''+'",\n"矩阵":'+grid+'}'
        print(gouxingstr)


        # msg_box = QMessageBox()
        # msg_box.setWindowTitle("构型名称录入窗口")
        # msg_box.setText("请输入构型名称:")

        # name_input = QLineEdit()
        # msg_box.setCheckBox(name_input) 

        # msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # ret = msg_box.exec_()
        # if ret == QMessageBox.Ok:
        #     name = name_input.text()
        #     # print("您输入的名称是:", name)
        #     msg_box = QMessageBox()
        #     msg_box.setWindowTitle("构型描述录入窗口")
        #     msg_box.setText("请输入构型的描述:")

        #     tips_input = QLineEdit()
        #     msg_box.setCheckBox(tips_input) 

        #     msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        #     ret = msg_box.exec_()
        #     if ret == QMessageBox.Ok:
        #         tips = tips_input.text()
        #         gouxingstr="{'构件':'"+name+"',\n'描述':'"+tips+"',\n'矩阵':'"+grid+"}"
        #         print(gouxingstr)

    def draw_edge(self):
        # 绘制边框线
        pen = QPen(Qt.black)
        pen.setWidth(2)
        self.addLine(0, 0, 0, self.GameOfLife.rows*self.GameOfLife.cell_size, pen) 
        self.addLine(0, 0, self.GameOfLife.cols*self.GameOfLife.cell_size, 0, pen)
        self.addLine(self.GameOfLife.cols*self.GameOfLife.cell_size, 0, self.GameOfLife.cols*self.GameOfLife.cell_size, self.GameOfLife.rows*self.GameOfLife.cell_size, pen)
        self.addLine(0, self.GameOfLife.rows*self.GameOfLife.cell_size, self.GameOfLife.cols*self.GameOfLife.cell_size, self.GameOfLife.rows*self.GameOfLife.cell_size, pen)

    def grid_to_str(self,grid):
        rows, cols = grid.shape
        gridstr = "["
        for i in range(rows):
            rowstr = "["
            for j in range(cols):
                val = grid[i,j]
                rowstr += str(int(val))
                if j < cols-1:
                    rowstr += ","
            gridstr += rowstr
            if i < rows-1:
                gridstr += "],\n"  
            else:
                gridstr += "]"  
        gridstr += "]"
        return gridstr


class InputDialog(QDialog):  
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        
        self.ok_button = QPushButton("确认")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.okaccept)
        self.cancel_button.clicked.connect(self.reject)
        
        form_layout = QFormLayout()
        form_layout.addRow("名称", self.name_input)
        form_layout.addRow("描述", self.desc_input)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        
    def okaccept(self):
        name = self.name_input.text()
        desc = self.desc_input.text()
        print(name, desc)
        if name=="" or desc=="":
            QMessageBox.warning(self, "警告", "名称和描述不能为空！")
            return
        # save_to_json(name, desc)
        self.close()
        return QDialog.Accepted
    # def reject(self):
    #     self.close()
    
def save_to_json(name, desc):
  # 保存到json文件
  pass

if __name__ == "__main__":
    app = QApplication([])
    dialog = InputDialog()
    dialog.show()
    app.exec_()

# view = GameView()
# scene = GameScene()
# view.setScene(scene)
