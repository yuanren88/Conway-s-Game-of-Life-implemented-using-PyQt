# Conway-s-Game-of-Life-implemented-using-PyQt
The Conway's Game of Life implemented using PyQt has full control over the game and map, including start, pause, reverse, clear, map parameter control and cell parameter control. It can customize game patterns and add them to the map.
# 康威生命游戏GUI
本程序实现了一个基于PyQt的康威生命游戏GUI界面。
## 特色
### 算法优化
实现初级的算法优化，使生命演变运算更加流畅
### 强大的场景操控力
提供对地图的多种操控，包括鼠标移动地图画布的控制，左键在世界自由添加构型的功能，鼠标左右键调整构型方向的控制，场景回退功能，地图放大缩小功能等等，让你轻松掌控整个生命世界
### 轻松构建构型库
基于json的游戏构型库，可以轻松增添和编辑构型；结合回退功能，让你轻易发现并捕获新的有意思的构型
## 界面组成
界面主要包含三个部分:
### 菜单栏
菜单栏包含一个文件菜单,可以开始、停止和刷新游戏。
### 工具栏 
工具栏提供快捷操作按钮,可以开始、停止、回退、刷新、清空等游戏操作。
### 游戏视图
游戏视图显示游戏格子状的网格区域,可以通过鼠标操作游戏，展示电子生命的演变。
## 功能操作
### 鼠标操作
- 左键点击可以添加或删除细胞
- 拖动可以移动模式
- 滚轮可以缩放格子大小
### 游戏控制
- 点击开始后游戏会自动循环执行
- 点击停止结束循环
- 通过回退按钮可以撤销上一步操作
- 刷新可以重绘界面
### 参数设置
可以通过设置按钮调整游戏参数,如格子大小等
### 模式添加
通过构型按钮可以添加预设的生命游戏模式
### 状态显示
状态栏显示游戏状态信息和鼠标位置坐标
## 使用方法
1. 添加构型库
2. 启动游戏 
3. 观察细胞生长变化规律
4. 操作鼠标调整生命构型
5. 设置参数自定义游戏
总之,该程序实现了一个功能完整的康威生命游戏GUI。




 # Conway's Game of Life GUI
This program implements a Conway's Game of Life GUI interface based on PyQt.
## Features
### Algorithm Optimization
Implement basic algorithm optimization to make the evolution of life smoother.
### Powerful Scene Control
Provide full control over the map, including mouse dragging to move the canvas, left click to freely add patterns in the world, left-right mouse buttons to adjust pattern directions, scene rollback function, zoom in and out of the map, etc. Easily control the whole life world. 
### Easy Construction of Pattern Library
Based on the json game pattern library, patterns can be easily added and edited; combined with the rollback function, you can easily discover and capture new interesting patterns.
## Interface Components
The interface mainly consists of three parts:
### Menu Bar 
The menu bar contains a file menu that can start, stop and refresh the game.
### Toolbar
The toolbar provides shortcut buttons to start, stop, rollback, refresh, clear etc. 
### Game View
The game view displays the gridded grid area of the game and can be operated with the mouse to show the evolution of cellular automata.
## Functional Operations
### Mouse Operations
- Left click to add or remove cells
- Drag to move patterns  
- Scroll wheel to zoom in and out
### Game Control
- The game will run automatically after starting
- Click stop to end the loop
- Use the rollback button to undo the previous step
- Refresh to redraw the interface
### Parameter Settings
Adjust game parameters such as grid size through setting buttons.  
### Pattern Addition
Add predefined life game patterns through pattern buttons.
### State Display  
The status bar displays game status information and mouse position coordinates.
## Usage
1. Add pattern library
2. Start the game
3. Observe the changes in cell growth patterns  
4. Operate the mouse to adjust life patterns
5. Customize the game with parameters
In summary, the program implements a fully functional Conway's Game of Life GUI.
