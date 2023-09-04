# import threading
# import numpy as np  
# import time
# import random
import cProfile

# def update_grid(self):
#     new_grid = self.grid.copy()
#     rows, cols = self.grid.shape
#     neighbors = np.zeros((rows, cols))
#     neighbors += np.roll(self.grid, 1, axis=0)  # 上方邻居
#     neighbors += np.roll(self.grid, -1, axis=0)  # 下方邻居
#     neighbors += np.roll(self.grid, 1, axis=1)  # 右方邻居
#     neighbors += np.roll(self.grid, -1, axis=1)  # 左方邻居
#     neighbors += np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1)  # 右上方邻居
#     neighbors += np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1)  # 右下方邻居
#     neighbors += np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1)  # 左上方邻居
#     neighbors += np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # 左下方邻居
#     total = neighbors / 1
    
#     new_grid[(self.grid == 1) & ((total < 2) | (total > 3))] = 0
#     new_grid[(self.grid == 0) & (total == 3)] = 1        
#     self.grid = new_grid
#     percentage=(self.grid.sum()/(self.rows*self.cols))*100
#     self.draw_grid()
#     self.status_label.setText("存活: {:.2f}%".format(percentage))
# if __name__ == "__main__":
#     profiler = cProfile.Profile()
#     profiler.enable()

#     update_grid(None)

#     profiler.disable()
#     profiler.print_stats()

import threading
import numpy as np
import numba

@numba.jit(nopython=True)
def update_grid(grid):
    new_grid = grid.copy()
    rows, cols = grid.shape
    neighbors = np.zeros((rows, cols))
    neighbors += np.roll(grid, 1, axis=0)  # 上方邻居
    neighbors += np.roll(grid, -1, axis=0)  # 下方邻居
    neighbors += np.roll(grid, 1, axis=1)  # 右方邻居
    neighbors += np.roll(grid, -1, axis=1)  # 左方邻居
    neighbors += np.roll(np.roll(grid, 1, axis=0), 1, axis=1)  # 右上方邻居
    neighbors += np.roll(np.roll(grid, -1, axis=0), 1, axis=1)  # 右下方邻居
    neighbors += np.roll(np.roll(grid, 1, axis=0), -1, axis=1)  # 左上方邻居
    neighbors += np.roll(np.roll(grid, -1, axis=0), -1, axis=1)  # 左下方邻居
    total = neighbors / 1
    
    new_grid[(grid == 1) & ((total < 2) | (total > 3))] = 0
    new_grid[(grid == 0) & (total == 3)] = 1        
    grid = new_grid
    return grid

class GameOfLife:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # self.grid = np.zeros((rows, cols))
        # 网格划分为4个区域
        self.grid = np.random.choice([0, 1], size=(self.rows,self. cols))
    def update_grid1(self):
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
        # percentage=(self.grid.sum()/(self.rows*self.cols))*100
        # self.draw_grid()
        # self.status_label.setText("存活: {:.2f}%".format(percentage))
   
    def calculate_neighbors(self):
        new_grid = self.grid.copy()
        rows, cols = self.grid.shape
        neighbors = np.zeros((rows, cols))
        n = list(range(8))

        def up():
            n[0]= np.roll(self.grid, 1, axis=0)  # 上方邻居
        def down():
            n[1]= np.roll(self.grid, -1, axis=0)  # 下方邻居
        def right():
            n[2]= np.roll(self.grid, 1, axis=1)  # 右方邻居
        def left():
            n[3]= np.roll(self.grid, -1, axis=1)  # 左方邻居
        def up_right():
            n[4]= np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1)  # 右上方邻居
        def up_left():
            n[5]= np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1)  # 左上方邻居
        def down_right():
            n[6]= np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1)  # 右下方邻居
        def down_left():
            n[7]= np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)  # 左下方邻居
        threads = []
        threads.append(threading.Thread(target=up))
        threads.append(threading.Thread(target=down))
        threads.append(threading.Thread(target=right))
        threads.append(threading.Thread(target=left))
        threads.append(threading.Thread(target=up_right))
        threads.append(threading.Thread(target=up_left))
        threads.append(threading.Thread(target=down_right))
        threads.append(threading.Thread(target=down_left))
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        for i in n:
            neighbors +=i
        total = neighbors / 1        
        new_grid[(self.grid == 1) & ((total < 2) | (total > 3))] = 0
        new_grid[(self.grid == 0) & (total == 3)] = 1        
        self.grid = new_grid
        # percentage=(self.grid.sum()/(self.rows*self.cols))*100
        # self.draw_grid()
        # self.status_label.setText("存活: {:.2f}%".format(percentage))

    def update_region(self,r1, r2, c1, c2):
        grid = self.grid[r1:r2, c1:c2]
        
        new_grid = grid.copy()
        
        # neighbors = calculate_neighbors(grid)  

        new_grid[(grid == 1) & ...] = 0 
        new_grid[(grid == 0) & ...] = 1

        self.grid[r1:r2, c1:c2] = new_grid

    def update_grid(self):
        ROWS = self.rows // 2  
        COLS = self.cols // 2

        threads = []

        t1 = threading.Thread(target=self.update_region, 
                args=(0, ROWS, 0, COLS))
        threads.append(t1)

        t2 = threading.Thread(target=self.update_region,  
                args=(0, ROWS, COLS, 2*COLS)) 
        threads.append(t2)

        t3 = threading.Thread(target=self.update_region,
                args=(ROWS, 2*ROWS, 0, COLS))
        threads.append(t3)

        t4 = threading.Thread(target=self.update_region, 
                args=(ROWS, 2*ROWS, COLS, 2*COLS))
        threads.append(t4)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.draw_grid()
    def draw_grid(self):
        print(self.grid)
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    g=GameOfLife(10000,10000)
    # g.draw_grid()
    # g.update_grid()
    for i in range(2):
        # g.calculate_neighbors()
        update_grid(g.grid)
    profiler.disable()
    profiler.print_stats()