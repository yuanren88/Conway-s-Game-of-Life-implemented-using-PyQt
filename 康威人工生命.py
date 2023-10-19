
import cProfile
import sys
import json
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsView, QMessageBox,QStyle,\
        QGraphicsScene,QMenuBar,QAction,QToolBar,QMainWindow,QSizePolicy,QStatusBar,QLabel,QGraphicsPixmapItem
from PyQt5.QtCore import QTimer, QRectF,Qt
from PyQt5.QtGui import QBrush, QColor,QPixmap,QIcon,QWheelEvent,QPainter
from PyQt5.QtWidgets import QGraphicsRectItem
from aboutform import AboutDialog
from settingform import SettingsDialog
from componentsForm import ComponentsDialog
from myviewscene import GameScene,GameView
from numba import jit

# todo 算法加速
# todo （完成）增加参数设置界面：界面长度，宽度，细胞大小，细胞颜色，细胞贴图。鼠标调整。时钟时间。
# todo （完成）界面调整：菜单，快捷按钮，底部菜单栏。。。
# todo （完成）功能：鼠标能够调整地图整体（未来3D地球化）。。。增加构形库，可以直接增加构型。
# todo 可变的地图：目前地图为长方形上下左右接通形态，未来，可以作出圆形，星型等异性地图，可以前后左右不接通，可以地图中增加高墙等。/
    # 每一个地图都是一个独立的类，包含各自的边界检测函数，或者是细胞变换函数，在世界构造初期通过类工厂进行载入。
# todo 增加地图编辑功能：增加地图编辑界面，可以设置复杂地图，增加，删除，移动地图中的高墙。
# todo 参见https://zhuanlan.zhihu.com/p/621070746
# todo （完成）可逆的元胞自动机，研究自动机的可逆性。。。。每一次演算进行地图保存是可行的，但是意义是什么呢（寻找有趣构型的每一个形态）？
# todo 三维的元胞自动机。引入新的grid，细胞算法和显示架构
# todo  游戏性：控制滑翔机穿越障碍。
# todo 研究寄存器机，尝试输出汉字。https://blog.csdn.net/Jailman/article/details/116230761
# todo 扩展生命规则：原生的康威生命游戏主要由两条规则构建：一，死亡细胞周围有3个存活细胞时就诞生为新细胞；二，存活细胞周围有2或3个存活细胞时就保持存活，否则死亡。这两条规则可以简记为B3/S23（其中，B代表出生，S代表存活）。通过修改B或S 后面的数字，就可以创建出不同的生命游戏。例如，把B1、B2、S3这三个开关打开，我们就创建了规则B12/S3，这意味着：死亡细胞周围有1或2个存活细胞时才诞生为新细胞，而存活细胞周围有3个存活细胞时才保持存活。
import threading
@jit(nopython=True)
def update_grid(grid,rows,cols):
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            total = int((grid[i, (j-1)%cols] + grid[i, (j+1)%cols] +
                        grid[(i-1)%rows, j] + grid[(i+1)%rows, j] +
                        grid[(i-1)%rows, (j-1)%cols] + grid[(i-1)%rows, (j+1)%cols] +
                        grid[(i+1)%rows, (j-1)%cols] + grid[(i+1)%rows, (j+1)%cols]) / 1)
            if grid[i, j] == 1:
                if total < 2 or total > 3:
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
    grid = new_grid
    return grid



# 创建一个新类，继承自QGraphicsPixmapItem
class PixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

class GameOfLife(QMainWindow):
    def __init__(self, rows=50, cols=95, cell_size=15):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.clock=100
        self.grid = np.random.choice([0, 1], size=(rows, cols))
        self.clicked_matrix= np.array([[1]])
        # 加载图片
        # self.black_pixmap = QPixmap("life.png")
        # self.white_pixmap = QPixmap("life.png")
        self.history = []  # 历史数组，用于存储每次绘制的grid
        self.Maxhistory = 1000  # 最大历史记录数
        self.isUndo=False
        self.black_brush = QBrush(QColor(0, 0, 0))
        self.white_brush = QBrush(QColor(255, 255, 255))
        self.dragging = False
        self.drag_start_pos = None
        self.run_count = 0

        self.settings=self.load_settings()
        # self.update_thread = GameThread(self)
        # self.update_thread.start()

        self.init_ui()
    def init_ui(self):
        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_grid)
        # self.timer.timeout.connect(lambda: update_grid(self.grid, self.rows, self.cols))
        self.timer.timeout.connect(self.run_update_grid)
        icon = QIcon('life.png')       
        # 创建菜单栏
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('文件')

        # 创建动作（Action）
        start_action = QAction('开始', self)
        start_action.triggered.connect(self.start_simulation)
        file_menu.addAction(start_action)

        stop_action = QAction('停止', self)
        stop_action.triggered.connect(self.stop_simulation)
        file_menu.addAction(stop_action)

        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh_simulation)
        file_menu.addAction(refresh_action)

        # 创建工具栏
        tool_bar = QToolBar(self)
        self.addToolBar(tool_bar)

        # 添加按钮到工具栏
        start_btn = QPushButton('开始', self)
        # start_btn.setIcon(QIcon('life.png'))
        start_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        start_btn.clicked.connect(self.start_simulation)
        tool_bar.addWidget(start_btn)

        step_btn = QPushButton('单步执行', self)
        step_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        step_btn.clicked.connect(self.run_update_grid)
        tool_bar.addWidget(step_btn)

        stop_btn = QPushButton('停止', self)
        stop_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        stop_btn.clicked.connect(self.stop_simulation)
        tool_bar.addWidget(stop_btn)

        self.undo_btn = QPushButton('回退', self)
        self.undo_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.undo_btn.clicked.connect(self.undo)
        tool_bar.addWidget(self.undo_btn)

        refresh_btn = QPushButton('刷新', self)
        refresh_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogOkButton))
        refresh_btn.clicked.connect(self.refresh_simulation)
        tool_bar.addWidget(refresh_btn)
        # 添加清空按钮
        clear_btn = QPushButton('清空', self)
        clear_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        clear_btn.clicked.connect(self.clear_grid)
        tool_bar.addWidget(clear_btn)

        # 添加设置按钮
        settings_btn = QPushButton('设置', self)
        settings_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        settings_btn.clicked.connect(self.show_settings)
        tool_bar.addWidget(settings_btn)

        # 添加构型按钮
        pattern_btn = QPushButton('构型', self)
        pattern_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))
        pattern_btn.clicked.connect(self.show_patterns)
        tool_bar.addWidget(pattern_btn)

        # 添加关于按钮
        about_btn = QPushButton('关于', self)
        about_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        about_btn.clicked.connect(self.show_about)
        tool_bar.addWidget(about_btn)

        # 添加退出按钮
        exit_btn = QPushButton('退出', self)
        exit_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        exit_btn.clicked.connect(self.close)
        tool_bar.addWidget(exit_btn)


        # 创建布局和视图
        layout = QVBoxLayout()
        # self.view = QGraphicsView(self)
        # self.scene = QGraphicsScene(self)
        self.scene=GameScene(self)
        self.view =GameView(self.scene)
        # self.view.setScene(self.scene)
        # self.view.setMouseTracking(True)  # 开启鼠标追踪
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为Expanding

        layout.addWidget(self.view)

        # 设置状态栏
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self.status_label = QLabel("地图："+str(self.cols)+'✖️'+str(self.rows), self)
        status_bar.addWidget(self.status_label)

        self.status_label2= QLabel("鼠标位置", self)
        status_bar.addWidget(self.status_label2)

        self.status_label3= QLabel("当前构型：一个活的元胞", self)
        status_bar.addWidget(self.status_label3)
        
        self.status_label4= QLabel("", self)
        status_bar.addWidget(self.status_label4)
       
        # 创建中央部件
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(tool_bar)
        central_layout.addLayout(layout)
        central_layout.addWidget(status_bar)

        self.setCentralWidget(central_widget)
        self.resize(1000, 800)
        self.setWindowTitle('模拟器')
        # self.setMouseTracking(True)
        # self.view.setMouseTracking(True)
    def Find_pattern(self):
        # 设定地图初始状态
        self.cols=200
        self.rows=200
        # 定义一个函数，用于生成所有可能的网格

        def gen_grids(r,c):
            grids=[]
            grid = np.zeros((r,c), dtype=int)
            total = 2**(r*c)
            for i in range(total):
                x = i
                grid[:,:] = 0
                for j in range(c*r):
                    grid.ravel()[j] = x%2
                    x //= 2
                # print(grid)
                if grid.sum() == 12:
                    grids.append(grid.copy())
            return grids

        # 调用函数，生成所有可能的3x3网格
        grids = gen_grids(5,5)
        count=0
        # 打印所有可能的网格
        for small_grid in grids:
            # print(grid)
            self.grid = np.zeros((self.rows, self.cols)) 
            self.add_grid(small_grid,50,50)
            # print(small_grid,'\n')
            runcount=0
            oldgrids=[]
            count+=1
            while runcount<12100:
                # 记录历史的grid
                oldgrids.append(self.grid.copy())
                if runcount>1:
                    oldgrids.pop(0)
                # 遍历产生不同的grid构型组合
                self.grid= update_grid(self.grid, self.rows, self.cols)

                sum=self.grid.sum()
                # or np.array_equal(oldgrids[0],self.grid)
                if (sum==0) or np.array_equal(oldgrids[0],self.grid):
                    # print('\nend in '+str(runcount)+' times')
                    break
                runcount+=1      
            if runcount>12000:      
                print('runcount',runcount)
                print(count,'/',len(grids),'\n')
                print(small_grid,'\n')

    def run_update_grid(self):
        self.grid= update_grid(self.grid, self.rows, self.cols)
        percentage=(self.grid.sum()/(self.rows*self.cols))*100
        self.run_count+=1
        self.status_label.setText("地图："+str(self.cols)+'✖️'+str(self.rows)+",轮次："+str(self.run_count)+",存活: {:.2f}%".format(percentage))
        self.draw_grid()

    def closeEvent(self, event):
        self.save_settings(self.settings)
        event.accept()

    # def init_ui(self):
    #     layout = QVBoxLayout()

    #     self.view = QGraphicsView(self)
    #     self.scene = QGraphicsScene(self)
    #     self.view.setScene(self.scene)
    #     self.view.setMouseTracking(True)  # 开启鼠标追踪

    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.update_grid)

    #     start_btn = QPushButton('Start', self)
    #     start_btn.clicked.connect(self.start_simulation)
    #     stop_btn = QPushButton('Stop', self)
    #     stop_btn.clicked.connect(self.stop_simulation)
    #     refresh_btn = QPushButton('Refresh', self)
    #     refresh_btn.clicked.connect(self.refresh_simulation)

    #     layout.addWidget(self.view)
    #     layout.addWidget(start_btn)
    #     layout.addWidget(stop_btn)
    #     layout.addWidget(refresh_btn)
    #     self.setLayout(layout)
    #     self.draw_grid()
    # def wheelEvent(self, event: QWheelEvent):
    #     print(event.angleDelta())
    #     if self.hasFocus():
    #         modifiers = QApplication.keyboardModifiers()
    #     # modifiers = QApplication.keyboardModifiers()
    #         if modifiers == Qt.ControlModifier:
    #             angle_delta = event.angleDelta().y()
    #             if angle_delta > 0:
    #                 self.cell_size += 1
    #             else:
    #                 self.cell_size = max(1, self.cell_size - 1)
    #             # self.refresh_simulation()
    #             print(self.cell_size)
    #             self.draw_grid()
    #         else:
    #             event.ignore()

    def shift_grid(self,grid, rows, cols):
        # 获取要平移的行数和列数
        num_rows = grid.shape[0]
        num_cols = grid.shape[1]

        # 创建一个新的空grid，用于存储平移后的结果
        new_grid = np.zeros_like(grid)

        # 计算平移后的行和列的索引
        new_rows = (np.arange(num_rows) + rows) % num_rows
        new_cols = (np.arange(num_cols) + cols) % num_cols

        # 使用索引赋值将原grid的数据平移到新的grid中
        new_grid[new_rows[:, np.newaxis], new_cols] = grid

        return new_grid
    
    def add_grid_with_dir(self, grid1, start_row, start_col, dir):
        '''
        增加方向调整功能的add_gird
        '''
        try:
            grid1=np.rot90(grid1, k=dir-1)
        except:
            gird1=grid1
        self.add_grid( grid1, start_row, start_col)


    def add_grid(self, grid1, start_row, start_col):
        
        # 获取grid1的形状
        rows1, cols1 = grid1.shape
        # rows1=grid1.shape[0]
        # cols1=grid1.shape[1]
        # 检查是否会越界
        if rows1>self.rows or cols1>self.cols:
            # 弹出警告
            QMessageBox.warning(self, "Warning", "构型太大，超过地图容纳范围。")
            raise ValueError("Insertion would exceed grid boundaries")
        # if end_row > self.grid.shape[0] or end_col > self.grid.shape[1]:
        #     raise ValueError("Insertion would exceed grid boundaries")
         
        # 计算平移的行列数,使grid1完全适应插入区域
        shift_rows = self.rows-max(self.rows, start_row+rows1) 
        shift_cols = self.cols-max(self.cols, start_col+cols1)

        # shift_rows = max(0, -start_row) 
        # shift_cols = max(0, -start_col)

        # 平移grid
        self.grid = self.shift_grid(self.grid, shift_rows, shift_cols)
        
        # 计算插入后的结束行列
        end_row = start_row + rows1
        end_col = start_col + cols1
        
           
        # 插入grid1
        # self.grid[start_row:end_row, start_col:end_col] = grid1
        self.grid[(start_row+shift_rows):(end_row+shift_rows), (start_col+shift_cols):(end_col+shift_cols)] = grid1
        
        # 平移回grid1原始位置
        self.grid = self.shift_grid(self.grid, -shift_rows, -shift_cols)
        
        # 返回平移后的grid1
        return grid1

    # 一次性增加一个矩阵的点
    def add_grid1(self, grid1,start_row,start_col):
    # 创建一个小的grid1
        # grid1 = np.array([[1, 1],
        #             [1, 1]])
#         grid1 = np.array([
#       [0, 1, 0],
#       [0, 0, 1],
#       [1, 1, 1]
#     ])
    # 定义要替换的区域在grid中的位置
        # start_row = 1
        # start_col = 2
        end_row = start_row + grid1.shape[0]
        end_col = start_col + grid1.shape[1]

        # 替换grid的对应区域
        self.grid[start_row:end_row, start_col:end_col] = grid1

    # def update_grid1(self):
    #     new_grid = self.grid.copy()
    #     rows, cols = self.grid.shape
    #     neighbors = np.zeros((rows, cols))
    #     n = list(range(8))
    #     def up():
    #         n[0]= np.roll(self.grid, 1, axis=0)  # 上方邻居
    #     def down():
    #         n[1]= np.roll(self.grid, -1, axis=0)  # 下方邻居
    #     def right():
    #         n[2]= np.roll(self.grid, 1, axis=1)  # 右方邻居
    #     def left():
    #         n[3]= np.roll(self.grid, -1, axis=1)  # 左方邻居
    #     def up_right():
    #         n[4]= np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1)  # 右上方邻居
    #     def up_left():
    #         n[5]= np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1)  # 左上方邻居
    #     def down_right():
    #         n[6]= np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1)  # 右下方邻居
    #     def down_left():
    #         n[7]= np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # 左下方邻居
    #     threads = []
    #     threads.append(threading.Thread(target=up))
    #     threads.append(threading.Thread(target=down))
    #     threads.append(threading.Thread(target=right))
    #     threads.append(threading.Thread(target=left))
    #     threads.append(threading.Thread(target=up_right))
    #     threads.append(threading.Thread(target=up_left))
    #     threads.append(threading.Thread(target=down_right))
    #     threads.append(threading.Thread(target=down_left))
    #     for t in threads:
    #         t.start()

    #     for t in threads:
    #         t.join()

    #     for i in n:
    #         neighbors +=i
    #     total = neighbors / 1        
    #     new_grid[(self.grid == 1) & ((total < 2) | (total > 3))] = 0
    #     new_grid[(self.grid == 0) & (total == 3)] = 1        
    #     self.grid = new_grid
    #     percentage=(self.grid.sum()/(self.rows*self.cols))*100
    #     self.draw_grid()
    #     self.status_label.setText("存活: {:.2f}%".format(percentage))


    # @jit(nopython=True)
    def update_grid(self):
        new_grid = self.grid.copy()
        rows, cols = self.grid.shape
        neighbors = np.zeros((rows, cols))
        neighbors += np.roll(self.grid, 1, axis=0)  # 上方邻居
        neighbors += np.roll(self.grid, -1, axis=0)  # 下方邻居
        neighbors += np.roll(self.grid, 1, axis=1)  # 右方邻居
        neighbors += np.roll(self.grid, -1, axis=1)  # 左方邻居
        neighbors += np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1)  # 右上方邻居
        neighbors += np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1)  # 右下方邻居
        neighbors += np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1)  # 左上方邻居
        neighbors += np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # 左下方邻居
        total = neighbors / 1
        
        new_grid[(self.grid == 1) & ((total < 2) | (total > 3))] = 0
        new_grid[(self.grid == 0) & (total == 3)] = 1        
        self.grid = new_grid
        percentage=(self.grid.sum()/(self.rows*self.cols))*100
        self.draw_grid()
        self.status_label.setText("地图："+str(self.cols)+'✖️'+str(self.rows)+",存活: {:.2f}%".format(percentage))

    # def update_grid(self):
    #     new_grid = self.grid.copy()
    #     for i in range(self.rows):
    #         for j in range(self.cols):
    #             total = int((self.grid[i, (j-1)%self.cols] + self.grid[i, (j+1)%self.cols] +
    #                         self.grid[(i-1)%self.rows, j] + self.grid[(i+1)%self.rows, j] +
    #                         self.grid[(i-1)%self.rows, (j-1)%self.cols] + self.grid[(i-1)%self.rows, (j+1)%self.cols] +
    #                         self.grid[(i+1)%self.rows, (j-1)%self.cols] + self.grid[(i+1)%self.rows, (j+1)%self.cols]) / 1)
    #             if self.grid[i, j] == 1:
    #                 if total < 2 or total > 3:
    #                     new_grid[i, j] = 0
    #             else:
    #                 if total == 3:
    #                     new_grid[i, j] = 1
    #     self.grid = new_grid
    #     self.draw_grid()  # 更新界面
   
    # def draw_grid(self):
    #     # self.scene.clear()
    #     self.Clear_grid()
    #     for i in range(self.rows):
    #         for j in range(self.cols):
    #             if self.grid[i, j] == 1:
    #                 brush = QBrush(QColor(0, 0, 0))
    #             else:
    #                 brush = QBrush(QColor(255, 255, 255))
    #             self.scene.addRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size, brush=brush)

    def draw_grid1(self):
        self.scene.clear()
        cells = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    pixmap = self.black_pixmap
                else:
                    pixmap = self.white_pixmap

                item = PixmapItem(pixmap)
                item.setPos(j * self.cell_size, i * self.cell_size)
                self.scene.addItem(item)

        # for cell in cells:
        #     self.scene.addItem(cell)
    def draw_grid(self):
        if  (self.isUndo==False)  :
            if (len(self.history) == 0) or not np.array_equal(self.grid, self.history[-1]) :
                self.history.append(self.grid.copy())
                self.isundoed=False
            # 如果历史数组的长度超过10，移除最早的元素
            if len(self.history) > self.Maxhistory:
                self.history = self.history[-self.Maxhistory:]
        self.isUndo=False
        # 改变undo_btn按钮展示名
        self.undo_btn.setText("回退"+"("+str(len(self.history))+")")
        
        # 创建双缓存的Pixmap
        pixmap = QPixmap(self.cols * self.cell_size, self.rows * self.cell_size)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        
        # 绘制网格
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    painter.fillRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size, Qt.black)
                # else:
                #     painter.fillRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size, Qt.white)

        painter.end()

        # 清除场景并添加绘制的Pixmap
        self.scene.clear()
        self.scene.draw_edge()
        self.scene.addPixmap(pixmap)
        if  self.cell_size>3:
            self.scene.draw_lines()

        # 更新视图
        self.view.update()



    # @jit(nopython=True)
    def draw_grid3(self):
        if  (self.isUndo==False)  :
            if (len(self.history) == 0) or not np.array_equal(self.grid, self.history[-1]) :
                self.history.append(self.grid.copy())
                self.isundoed=False
            # 如果历史数组的长度超过10，移除最早的元素
            if len(self.history) > self.Maxhistory:
                self.history = self.history[-self.Maxhistory:]
        self.isUndo=False
        # 改变undo_btn按钮展示名
        self.undo_btn.setText("回退"+"("+str(len(self.history))+")")
        
        # self.scene=GameScene(self)        
        # self.view.setScene(self.scene)
        self.scene.clear()
        self.cells = []
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 1:
                    brush = self.black_brush
                    rect = QGraphicsRectItem(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    rect.setBrush(brush)
                    self.cells.append(rect)
                else:
                    brush = self.white_brush
                # rect = QGraphicsRectItem(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                # rect.setBrush(brush)
                # self.cells.append(rect)

        for cell in self.cells:
            self.scene.addItem(cell)
        
        # print(len(cells))

    def show_settings(self):
        self.timer.stop()
        dialog = SettingsDialog(self)
        dialog.length_edit.setText(str(self.cols))
        dialog.width_edit.setText(str(self.rows))
        dialog.cell_size_edit.setText(str(self.cell_size))
        dialog.clock_edit.setText(str(self.clock))
        dialog.mycolor=QColor(0, 0, 0)#self.black_brush.color
        if dialog.exec_():
            self.cols = int(dialog.length_edit.text())
            self.rows = int(dialog.width_edit.text())
            self.cell_size = int(dialog.cell_size_edit.text())
            self.grid = np.random.choice([0, 1], size=(self.rows, self.cols))
            self.clock = int(dialog.clock_edit.text())
            self.black_brush=QBrush(dialog.mycolor)
            # self.white_brush=QBrush(QColor(255, 255, 255))
            # 更新timer的clock
            self.timer.setInterval(self.clock)
            # self.status_label = QLabel("地图："+str(self.cols)+'✖️'+str(self.rows), self)
            percentage=(self.grid.sum()/(self.rows*self.cols))*100
            self.status_label.setText("地图："+str(self.cols)+'✖️'+str(self.rows)+",轮次："+str(self.run_count)+",存活: {:.2f}%".format(percentage))

            self.draw_grid()



    def clear_grid(self):
        self.grid = np.zeros((self.rows, self.cols))
        self.draw_grid()


    def show_patterns(self):
        # 显示构型窗口的逻辑...
        ComponentsD=ComponentsDialog(self)
        result = ComponentsD.exec_()
        if result == 0:
            self.clicked_matrix = np.array(ComponentsD.clicked_matrix)
            self.status_label3.setText('当前构型：'+ComponentsD.component)

        # self.grid= self.shift_grid(self.grid,-1,-1)
        # self.draw_grid()

    def undo(self):
            # 回退操作
        if len(self.history) > 1:
            # if self.isundoed==False:
            #     self.history.pop()
            self.grid = self.history.pop()
            # self.history = self.history[:-1]
            self.isUndo=True
            self.draw_grid()
            self.isundoed=True
    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()
    def one_step(self):
        self.update()
        self.draw_grid()
    def start_simulation(self):
        self.timer.start(self.clock)
    def stop_simulation(self):
        self.timer.stop()
    def refresh_simulation(self):
        self.grid = np.random.choice([0, 1], size=(self.rows,self. cols))
        self.draw_grid()
    def load_settings(self):
        with open('settings.json') as f:
            settings = json.load(f)
            self.cols=int(settings["cols"])
            self.rows=int(settings["rows"])
            self.clock=int(settings["clock"])
            self.black_brush= QBrush(QColor((settings["color"])))     
            self.cell_size=int(settings["cell_size"])
            # self.grid = np.random.choice([0, 1], size=(self.rows, self.cols))
            # self.grid = np.fromstring(settings["grid"], dtype=int).reshape(self.rows, self.cols)
            data = np.load('grid.npz')
            self.grid = data['grid'].astype(np.int)             
            return settings

    def save_settings(self,settings):
        with open('settings.json', 'w') as f:
            settings["cols"]=self.cols
            settings["rows"]=self.rows
            settings["clock"]=self.clock
            settings["color"]=self.black_brush.color().name()
            settings["cell_size"]=self.cell_size
            np.savez_compressed('grid.npz', grid=self.grid)
            json.dump(settings, f)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_of_life = GameOfLife()


    game_of_life.show()
    game_of_life.draw_grid()
    grid=np.random.choice([0, 1], size=(1, 1))
    update_grid(grid,1,1)
    profiler = cProfile.Profile()
    profiler.enable()
    # Find_pattern(100,100)
    # game_of_life.Find_pattern()
    # for i in range(20):
    #     game_of_life.run_update_grid()
        # game_of_life.update_grid()
    #     update_grid(game_of_life.grid, game_of_life.rows, game_of_life.cols)

    profiler.disable()
    # profiler.print_stats()

    sys.exit(app.exec_())


    