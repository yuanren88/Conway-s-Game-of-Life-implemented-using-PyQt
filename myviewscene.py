from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent
class GameView(QGraphicsView):
    def __init__(self,scene):
        super().__init__()
        self.setMouseTracking(True)
        self.scene = scene
        self.setScene(scene)
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
    def mousePressEvent(self, event):
        print(event.button())
        # self.direction=1
        self.draged=False
        if event.button() == Qt.LeftButton:
            global_pos = event.globalPos()
            view_pos = self.GameOfLife.view.mapFromGlobal(global_pos)
            self.dragging = True
            self.drag_start_pos = view_pos  #event.pos()
            # print(self.drag_start_pos)
        if event.button() ==2:
            self.direction += 1
            if self.direction > 4:
                self.direction = 1  
            print('dir'+str(self.direction))          
        # elif event.button() == Qt.RightButton:
        #     # 左键已经按下的情况下,再点击右键调整方向
        #     if self.dragging:  
        #         self.direction += 1
        #         if self.direction > 4:
        #             self.direction = 1
    def mouseMoveEvent(self, event):
        # print(event.pos())
        global_pos = event.globalPos()
        view_pos = self.GameOfLife.view.mapFromGlobal(global_pos)
        row = int((view_pos.y() ) // self.GameOfLife.cell_size)
        col = int((view_pos.x() ) // self.GameOfLife.cell_size)    

        self.GameOfLife.status_label2.setText('位置：'+str(col)+' '+str(row))
        if self.dragging:
            delta = view_pos- self.drag_start_pos
            # delta = event.pos() - self.drag_start_pos
            row_offset = delta.y() // self.GameOfLife.cell_size
            col_offset = delta.x() // self.GameOfLife.cell_size
            # print(row_offset, col_offset)
            if row_offset!=0 or col_offset!=0:
                self.GameOfLife.grid =self.GameOfLife.shift_grid(self.GameOfLife.grid, row_offset, col_offset)
                self.drag_start_pos = event.pos()
                self.GameOfLife.draw_grid()
                self.draged=True

    def mouseReleaseEvent(self, event):
        
        if event.button() == Qt.LeftButton:
            self.dragging = False
            if not self.draged:
                row = int((self.drag_start_pos.y() ) // self.GameOfLife.cell_size)
                col = int((self.drag_start_pos.x() ) // self.GameOfLife.cell_size)    
                # self.GameOfLife.add_grid(self.GameOfLife.clicked_matrix, row, col)
                self.GameOfLife.add_grid_with_dir(self.GameOfLife.clicked_matrix, row, col,self.direction)
                self.GameOfLife.draw_grid()
                self.direction=1

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
        print(self.GameOfLife.cell_size)
        self.GameOfLife.draw_grid()
        # else:
        #     event.ignore()


    
# view = GameView()
# scene = GameScene()
# view.setScene(scene)
