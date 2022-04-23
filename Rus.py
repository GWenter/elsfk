#!/D:/path/ python
# -*- coding: UTF-8 -*-
#
# @Project : elsfk
# @File    : Rus.py
# @Date    :2022/4/13 : 18:34

# -*- coding: utf-8 -*-
import pandas as pd
import csv
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
import random

seven_shapes = [
    [[[0, 0], [0, 1], [-1, 0], [-1, 1]],
     [[0, 0], [0, 1], [-1, 0], [-1, 1]],
     [[0, 0], [0, 1], [-1, 0], [-1, 1]],
     [[0, 0], [0, 1], [-1, 0], [-1, 1]]],

    [[[-1, -1], [0, 1], [0, 2], [0, 3]],
     [[1, 1], [-1, 0], [-2, 0], [-3, 0]],
     [[-1, -1], [0, 1], [0, 2], [0, 3]],
     [[1, 1], [-1, 0], [-2, 0], [-3, 0]]],

    [[[0, 0], [-1, -1], [-1, 0], [-1, 1]],
     [[1, 0], [-1, 0], [-2, 0], [-1, -1]],
     [[-1, -1], [0, 1], [0, 2], [-1, 1]],
     [[0, 1], [-1, 0], [-2, 0], [-1, 1]]],

    [[[-1, 0], [-1, 0], [-1, 1], [-1, 2]],
     [[1, 1], [-2, -1], [-2, 0], [-1, 0]],
     [[0, -1], [0, 1], [0, 2], [-1, 2]],
     [[0, 0], [0, 1], [-1, 0], [-2, 0]]],

    [[[2, 2], [-1, 0], [-1, -1], [-1, -2]],
     [[0, -2], [0, 1], [-1, 1], [-2, 1]],
     [[0, 0], [0, 1], [0, 2], [-1, 0]],
     [[-2, 0], [-1, 0], [-2, 0], [-2, 1]]],

    [[[0, 0], [0, 1], [-1, -1], [-1, 0]],
     [[0, 0], [-1, 0], [-1, 1], [-2, 1]],
     [[0, 0], [0, 1], [-1, -1], [-1, 0]],
     [[0, 0], [-1, 0], [-1, 1], [-2, 1]]],

    [[[-1, -1], [0, 1], [-1, 2], [-1, 1]],
     [[1, 1], [-1, 0], [-1, -1], [-2, -1]],
     [[-1, -1], [0, 1], [-1, 2], [-1, 1]],
     [[1, 1], [-1, 0], [-1, -1], [-2, -1]]]
]

# seven_shapes[x]为七个组件，分别是O，I，T，L，J，Z，S七种形态。每个组件含有四种转向。
# seven_shapes[x][0]为初始转向状态，seven_shapes[x][1]为下一个顺时针90度转向状态，以此类推，一共四个。
# seven_shapes[x][0][1]为1号随从格的相对坐标，以此类推，随从格一共有三个。
# seven_shapes[x][0][0]为旋转偏差值。
# seven_shapes[x][0][0][0]为逆时针偏差值。
# seven_shapes[x][0][0][1]为顺时针偏差值。

now_and_next_shape = []  # 存放当前和之后的2个shape


class Rus:

    """ 俄罗斯方块游戏  """

    def __init__(self):
        """ 游戏参数设置 """
        self.FPS = 300  # 降落速度 1000 = 1秒
        self.col_cells = 12  # 一行多少个单元格(含边框)
        self.row_cells = 24  # 一共多少行单元格(含边框)
        self.canvas_bg = 'white'  # 游戏背景色
        self.cell_gap = 1  # 方格间距
        self.frame_x = 5  # 左右边距
        self.frame_y = 5  # 上下边距
        self.win_w_plus = 280  # 窗口右边额外多出的宽度
        self.color_dict = {0: '#e0e0e0',  # 0表示空白
                           1: '#000000',  # 1为已落地的方块色
                           2: 'green',  # 2为定位格
                           3: 'green',  # 3为组件中除了定位格剩下的三个单元格
                           4: '#b3b3b3'}  # 4代表边框

        self.run_game()

    def window_center(self, window, w_size, h_size):
        """ 窗口居中 """
        screenWidth = window.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = window.winfo_screenheight()  # 获取显示区域的高度
        left = (screenWidth - w_size) // 2
        top = (screenHeight - h_size) // 2 - 10
        window.geometry("%dx%d+%d+%d" % (w_size, h_size, left, top))

    def create_map(self, col, row):
        """ 创建地图列表 """
        global game_map
        game_map = []
        for y in range(0, col):
            game_map.append([])
        for y in range(0, col):
            for x in range(0, row):
                game_map[y].append(x)
                game_map[y][x] = 0  # 生成一个全是0的空数列

    def create_wall(self):
        """ 绘制边框 """  # 除了顶部，三个边全部是边框
        for i in range(0, self.col_cells - 1):
            game_map[self.row_cells - 1][i] = 4

        for i in range(0, self.row_cells - 1):
            game_map[i][0] = 4
            game_map[i][self.col_cells - 1] = 4

        game_map[-1][-1] = 4

    def create_canvas(self):
        """ 创建画布 """
        global canvas, window
        canvas_h = cell_size * self.row_cells + self.frame_y * 2
        canvas_w = cell_size * self.col_cells + self.frame_x * 2

        canvas = tk.Canvas(window,
                           bg=self.canvas_bg,
                           height=canvas_h,
                           width=canvas_w,
                           highlightthickness=0)

    def fresh_cells(self):
        """ 刷新单元格 """
        for y in range(0, self.row_cells):
            for x in range(0, self.col_cells):
                a = self.frame_x + cell_size * x
                b = self.frame_y + cell_size * y
                c = self.frame_x + cell_size * (x + 1)
                d = self.frame_y + cell_size * (y + 1)
                e = self.canvas_bg
                f = self.cell_gap
                g = self.color_dict[game_map[y][x]]

                canvas.itemconfig(canvas.create_rectangle(a, b, c, d, outline=e, width=f, fill=g),
                                  fill=g)
        canvas.place(x=0, y=0)

    def random_shape(self):
        """ 生成随机的shape """
        global turn_times
        turn_times = 0  # 翻转的次数
        x_shape = random.randint(0, 6)  # 七个组件随机出现
        now_and_next_shape.append(x_shape)

    def get_locator_cell_pos(self):
        """ 获取定位格坐标 """  # 每个shape由4个单元格组成，一个定位格和三个随从单元格
        global shape_x, shape_y
        xy = []
        for i in range(0, self.row_cells):
            try:  # 查找数值为2的坐标，没有就返回0。为防止在0列，先加上1，最后再减去。
                x = game_map[i].index(2) + 1
            except:
                x = 0
            xy.append(x)
        shape_x = max(xy)
        shape_y = xy.index(shape_x)
        shape_x = shape_x - 1  # 之前加1，现在减回

    def get_follow_cells_pos(self, a, b):  # 每个shape由4个单元格组成，一个定位格和三个随从单元格
        """ 三个随从单元格的坐标。a为当前或是下一个shape，b是旋转次数 """
        global y1, x1, y2, x2, y3, x3
        y1 = seven_shapes[now_and_next_shape[a]][b][1][0]
        x1 = seven_shapes[now_and_next_shape[a]][b][1][1]
        y2 = seven_shapes[now_and_next_shape[a]][b][2][0]
        x2 = seven_shapes[now_and_next_shape[a]][b][2][1]
        y3 = seven_shapes[now_and_next_shape[a]][b][3][0]
        x3 = seven_shapes[now_and_next_shape[a]][b][3][1]

    def creat_mini_canvas(self):
        """ 创建预览图用的mini canvas """
        global canvas2
        canvas2 = tk.Canvas(window, bg=self.canvas_bg,
                            height=cell_size * 2 + self.frame_y * 2,
                            width=cell_size * 4 + self.frame_x * 2,
                            highlightthickness=0)

    def creat_mini_map(self):
        """ 创建预览图 """
        mini_map = []
        for y in range(0, 2):
            mini_map.append([])
        for y in range(0, 2):
            for x in range(0, 4):
                mini_map[y].append(x)
                mini_map[y][x] = 0  # 生成一个全是0的空数列

        l0 = [1, 0, 1, 0, 2, 1, 0]  # 七个组件每个初始出现的X坐标值
        y0 = 1  # 初始的Y坐标值
        x0 = l0[now_and_next_shape[1]]  # 初始的X坐标值

        # 其余三个shape的坐标
        self.get_follow_cells_pos(1, 0)  # 1是下一个shape，0是旋转的次数

        mini_map[y0][x0] = 1
        mini_map[y0 + y1][x0 + x1] = 1
        mini_map[y0 + y2][x0 + x2] = 1
        mini_map[y0 + y3][x0 + x3] = 1

        for y in range(0, 2):
            for x in range(0, 4):
                canvas2.itemconfig(canvas2.create_rectangle(self.frame_x + cell_size * x,
                                                            self.frame_y + cell_size * y,
                                                            self.frame_x + cell_size * (x + 1),
                                                            self.frame_y + cell_size * (y + 1),
                                                            outline=self.canvas_bg,
                                                            width=self.cell_gap),
                                   fill=self.color_dict[mini_map[y][x]])

        canvas2.place(x=cell_size * self.col_cells + cell_size * 2, y=cell_size * 2)

    def follow_cells_bind_to_locator(self, x, a):  # 三个随从格绑定与定位格的坐标
        """ x为turn_times的翻转值，a为单元格的颜色代码 """
        self.get_locator_cell_pos()

        l0 = [5, 4, 5, 5, 6, 5, 5]  # 七个组件每个初始出现的X坐标值
        y0 = 1  # 初始的Y坐标值
        x0 = l0[now_and_next_shape[0]]  # 初始的X坐标值

        self.get_follow_cells_pos(0, x)

        if shape_x != -1:  # 等于-1的话就代表没有shape，不是刚开始就是刚落地
            if game_map[shape_y + y1][shape_x + x1] in [0, 2, 3] and \
                    game_map[shape_y + y2][shape_x + x2] in [0, 2, 3] and \
                    game_map[shape_y + y3][shape_x + x3] in [0, 2, 3]:
                game_map[shape_y + y1][shape_x + x1] = a
                game_map[shape_y + y2][shape_x + x2] = a
                game_map[shape_y + y3][shape_x + x3] = a
        else:  # 出现在画面顶端
            game_map[y0][x0] = 2
            game_map[y0 + y1][x0 + x1] = 3
            game_map[y0 + y2][x0 + x2] = 3
            game_map[y0 + y3][x0 + x3] = 3

        self.get_locator_cell_pos()

    def Release_speed(self, event):
        """ 上下键释放 """  # 弹起上键或下键，触发速度的改变

        def speed_Release(up, down):
            """ 上下键释放 """
            global speed
            direction = event.keysym
            if (direction == up):
                speed[0] = 0
            if (direction == down):
                speed[0] = 0

        speed_Release('w', 's')

    def shape_move(self, x, y, z):
        """ shape移动。x，y为XY轴的偏移，z为颜色代码（当前shape或是已落地的shape，1或3） """
        self.follow_cells_bind_to_locator(turn_times, 0)  # 把三个随从格颜色变成0，即删除
        game_map[shape_y + 0][shape_x + 0] = 0  # 把定位格颜色变为0，即删除
        game_map[shape_y + y][shape_x + x] = 2  # X轴或Y轴移动一格后生成新的定位格
        self.follow_cells_bind_to_locator(turn_times, z)  # 根据新的定位格坐标生成随从格，颜色是1或者是3（当前shape或已落地的shape）

    def control_shape(self, event):
        """ 操控shape """

        def speed_key(up, down):
            """ 上下键控制速度 """
            global speed
            direction = event.keysym
            if (direction == up):
                speed[0] = 1
            elif (direction == down):
                speed[0] = 2
            else:
                speed[0] = 0

        def move_key(key, x):
            """ 左右移动按键，x为左右移动数 """
            global turn_times
            direction = event.keysym
            if (direction == key):
                self.get_follow_cells_pos(0, turn_times)
                # 如果遇上墙或者已固定的方块，则不做移动
                if game_map[shape_y + 0][shape_x + 0 + x] in [1, 4] or \
                        game_map[shape_y + y1][shape_x + x1 + x] in [1, 4] or \
                        game_map[shape_y + y2][shape_x + x2 + x] in [1, 4] or \
                        game_map[shape_y + y3][shape_x + x3 + x] in [1, 4]:
                    pass
                else:
                    self.shape_move(x, 0, 3)

        def clockwise_key(key):
            """ 顺时针转向按键 """
            global turn_times
            direction = event.keysym
            if (direction == key):
                turn_times = turn_times + 1  # 旋转次数，每旋转一次数值加1
                if turn_times > 3:  # 总共4个转向，大于3就变回0
                    turn_times = 0

                x4 = seven_shapes[now_and_next_shape[0]][turn_times][0][1]
                self.follow_cells_bind_to_locator(turn_times - 1, 0)
                self.shape_move(x4, 0, 3)

        def counterclockwise_key(key):
            """ 逆时针转向按键 """
            global turn_times
            direction = event.keysym
            if (direction == key):
                turn_times = turn_times - 1
                if turn_times < 0:  # 和顺时针相反，小于0就变成3
                    turn_times = 3

                x4 = seven_shapes[now_and_next_shape[0]][turn_times][0][0]

                if turn_times < 3:
                    self.follow_cells_bind_to_locator(turn_times + 1, 0)
                else:
                    self.follow_cells_bind_to_locator(0, 0)

                self.shape_move(x4, 0, 3)

        def pause_key(key):
            """ 暂停键 """
            global loop, gloop
            direction = event.keysym
            if (direction == key):
                loop = 0
                showinfo('暂停', '按确定键继续')
                loop = 1
                gloop = window.after(FPS, self.game_loop)

        def clockwise_key_estimate():
            """ 顺时针转向判断 """  # 如果遇上墙或者已完成的方块，阻止其转向
            x = turn_times + 1
            if x > 3:
                x = 0

            x0 = seven_shapes[now_and_next_shape[0]][x][0][1]
            self.get_follow_cells_pos(0, x)

            if shape_y + y1 > 0 or shape_y + y2 > 0 or shape_y + y3 > 0:
                if game_map[shape_y + 0][shape_x + x0 + 0] in [1, 4] or \
                        game_map[shape_y + y1][shape_x + x0 + x1] in [1, 4] or \
                        game_map[shape_y + y2][shape_x + x0 + x2] in [1, 4] or \
                        game_map[shape_y + y3][shape_x + x0 + x3] in [1, 4]:
                    self.shape_move(0, 0, 3)
                else:
                    clockwise_key('j')

        def counterclockwise_estimate():
            """ 逆时针转向判断 """  # 如果遇上墙或者已完成的方块，阻止其转向
            x = turn_times - 1
            if x < 0:
                x = 3

            x0 = seven_shapes[now_and_next_shape[0]][x][0][0]
            self.get_follow_cells_pos(0, x)

            if shape_y + y1 > 0 or shape_y + y2 > 0 or shape_y + y3 > 0:
                if game_map[shape_y + 0][shape_x + x0 + 0] in [1, 4] or \
                        game_map[shape_y + y1][shape_x + x0 + x1] in [1, 4] or \
                        game_map[shape_y + y2][shape_x + x0 + x2] in [1, 4] or \
                        game_map[shape_y + y3][shape_x + x0 + x3] in [1, 4]:
                    self.shape_move(0, 0, 3)
                else:
                    counterclockwise_key('k')

        move_key('a', -1)
        move_key('d', 1)

        speed_key('w', 's')
        pause_key('p')

        clockwise_key_estimate()
        counterclockwise_estimate()
        self.fresh_cells()

    def auto_down(self):
        """ 组件自动下降 """
        global turn_times, FPS
        self.get_follow_cells_pos(0, turn_times)
        # 当前shape下方是墙或者是已完成的shape，那当前shape变成已完成的状态，即值等于1
        if game_map[shape_y + 0 + 1][shape_x + 0] in [1, 4] or \
                game_map[shape_y + y1 + 1][shape_x + x1] in [1, 4] or \
                game_map[shape_y + y2 + 1][shape_x + x2] in [1, 4] or \
                game_map[shape_y + y3 + 1][shape_x + x3] in [1, 4]:
            self.shape_move(0, 0, 1)  # 三个随从格变成1
            game_map[shape_y][shape_x] = 1  # 定位格也变成1

            del now_and_next_shape[0]  # 删除当前shape，准备出现下一个
            self.random_shape()  # 再随机创建一个新的shape
            canvas2.delete('all')  # 清除预览图的canvas，创建过多会有BUG
            self.creat_mini_map()
            self.follow_cells_bind_to_locator(0, 3)
            speed[0] = 0
            FPS = self.FPS
        else:
            self.shape_move(0, 1, 3)

    def full_del(self):
        """ 满行清除并新增一行 """
        global r1, r2, r3, r4
        r = 0  # 一次消除的行数
        for i in range(1, self.row_cells - 1):  # 某行若出现10个1，就删除该行，并在第2行之后再插入一行空的
            if game_map[i].count(1) == self.col_cells - 2:
                del game_map[i]
                r = r + 1
                new_row = []  # 准备要插入的新行
                for x in range(0, self.col_cells):
                    new_row.append(0)
                new_row[0] = 4  # 第一格和最后一格是边框
                new_row[-1] = 4
                game_map.insert(2, new_row)

        if r == 1:  # 本次一共消除了一行
            r1 = r1 + 1
        elif r == 2:  # 本次一共消除了二行
            r2 = r2 + 1
        elif r == 3:  # 本次一共消除了三行
            r3 = r3 + 1
        elif r == 4:  # 本次一共消除了四行
            r4 = r4 + 1

    def scoring(self):
        """ 计分牌 """
        global scoring_lable
        scoring_lable = tk.Label(window, text="", font=('Yahei', 12), anchor="ne", justify="left")

        scoring_lable.place(x=cell_size * self.col_cells + cell_size * 2,
                            y=cell_size * 16)

    def scoring_loop(self):
        """ 计分更新 """
        global r5, r6, scoring_lable
        r5 = r1 + r2 * 2 + r3 * 3 + r4 * 4  # 消除的总数
        r6 = r1 + r2 * 2 * 2 + r3 * 3 * 3 + r4 * 4 * 4  # 计分。消的越多，奖励越多

        scoring_lable['text'] = "\n" \
                                + "\n单消： " + str(r1) \
                                + "\n双消： " + str(r2) \
                                + "\n三消： " + str(r3) \
                                + "\n四消： " + str(r4) \
                                + "\n" \
                                + "\n总消： " + str(r5) \
                                + "\n总分： " + str(r6)

    def game_over(self):
        """ 游戏结束 """
        global r1, r2, r3, r4, r5, r6, scoring_lable
        if game_map[2].count(1) > 0:  # 有1出现了就算失败
            showinfo('游戏结束', '得分为 {} 分'.format(r6))
            scoring_lable['text'] = ''
            self.save_rank()
            self.game_start()

    def save_rank(self):
        """ 存分数  格式为[时间，分数]"""
        global r6, r4, r3, r2, r1
        now = datetime.now()
        with open('rank.csv', 'a+', encoding='utf-8') as fd:
            list_ = [[str(now), r6, r4, r3, r2, r1]]
            writer = csv.writer(fd)
            writer.writerows(list_)

    def game_loop(self):
        """ 游戏循环刷新 """
        global window, FPS, gloop
        canvas.delete('all')  # 清除canvas，不清除的话时间久了有BUG
        self.fresh_cells()
        self.auto_down()
        self.full_del()
        self.scoring_loop()

        if speed[0] == 1:  # 值为1时，速度减慢
            FPS = self.FPS * 5
        elif speed[0] == 2:  # 值为2时，速度加快
            FPS = 20
        else:
            FPS = self.FPS

        self.game_over()

        if loop == 1:  # 暂停开关
            gloop = window.after(FPS, self.game_loop)

    def game_start(self):
        """ 初始化游戏 """
        global window, speed, FPS, loop, r1, r2, r3, r4, r5, r6
        r1 = 0  # 消除一行的次数
        r2 = 0  # 消除二行的次数
        r3 = 0  # 消除三行的次数
        r4 = 0  # 消除四行的次数
        r5 = 0  # 消除的总数
        r6 = 0  # 计分

        loop = 0  # 暂停开关。1为开启，0为暂停
        speed = [0]  # 速度调节参数
        self.create_map(self.row_cells, self.col_cells)
        self.create_wall()
        self.random_shape()
        self.random_shape()  # 执行2次，生成2个随机的shape
        self.creat_mini_canvas()
        self.creat_mini_map()
        self.follow_cells_bind_to_locator(0, 3)
        window.bind('<KeyPress>', self.control_shape)
        window.bind('<KeyRelease>', self.Release_speed)
        FPS = self.FPS
        self.create_canvas()
        self.scoring()
        self.game_loop()

        def close_w():
            if loop == 1:
                window.after_cancel(gloop)
            window.destroy()

        window.protocol('WM_DELETE_WINDOW', close_w)
        window.mainloop()

    def pause_but(self):
        """ 暂停函数控制按钮 """

        global loop, gloop
        loop = 0
        showinfo('暂停/开始', '暂停/开始')
        loop = 1
        gloop = window.after(FPS, self.game_loop)

    def restart_but(self):
        """ 重新开始按钮 """
        global loop
        loop = 0
        if askyesno('重新开始', '确定重新开始吗？'):
            self.game_start()

    def quit_but(self):
        """ 暂停按钮 """
        global loop
        loop = 0
        if askyesno('确定游戏', '确定退出吗？'):
            exit()

    def rank_but(self):
        global  loop
        loop = 0
        data = pd.read_csv('rank.csv')
        rank_ = data.sort_values(by=['分数', '四消', '三消', '双消', '单消'], ascending=False)
        list_ = []
        for i in range(0, len(rank_)):
            rank_list = i
            zf = rank_.iloc[i]['分数']
            sx = rank_.iloc[i]['四消']
            list_.append([rank_list, zf, sx])
        rank_window = tk.Tk()
        rank_window.title('排行榜')
        screenHeight =rank_window.winfo_screenheight()  # 获取显示区域的高度
        cell_size = screenHeight / (self.row_cells + 5)

        win_w_size = 2 * cell_size + self.frame_x * 2 + self.win_w_plus
        win_h_size = 10 * cell_size + self.frame_y * 2

        self.window_center(rank_window, win_w_size, win_h_size)
        rank_text = Listbox(rank_window)
        rank_text.pack()
        for i in range(0, len(rank_)):
            rank_text.insert(i, list_[i])
        rank_text.insert(0, ['rank', '得分', '四消'])
        rank_window.mainloop()

    def run_game(self):
        """ 开启游戏 """
        global window, cell_size, gloop

        window = tk.Tk()
        window.focus_force()
        window.title('俄罗斯方块')
        window.resizable(0, 0)  #窗口大小控制为不能改变
        gloop = None
        screenHeight = window.winfo_screenheight()  # 获取显示区域的高度
        cell_size = screenHeight / (self.row_cells + 5)

        win_w_size = self.col_cells * cell_size + self.frame_x * 2 + self.win_w_plus
        win_h_size = self.row_cells * cell_size + self.frame_y * 2

        self.window_center(window, win_w_size, win_h_size)

        rank_but = Button(window, text='排行榜', bg='yellow', height=1, width=12, font=('Yahei', 12), command=self.rank_but)
        rank_but.place(x=cell_size * self.col_cells + cell_size * 2,
                       y=cell_size * 9)

        pause_but = Button(window, text='开始/暂停', bg='light green', height=1, width=12, font=('Yahei', 12), command=self.pause_but)
        pause_but.place(x=cell_size * self.col_cells + cell_size * 2,
                        y=cell_size * 11)

        start_but = Button(window, text='重新开始', height=1, width=12, font=('Yahei', 12), command=self.restart_but)
        start_but.place(x=cell_size * self.col_cells + cell_size * 2,
                        y=cell_size * 13)

        quit_but = Button(window, text='退出', bg='red', height=1, width=12, font=('Yahei', 12), command=self.quit_but)
        quit_but.place(x=cell_size * self.col_cells + cell_size * 2,
                       y=cell_size * 15)

        self.game_start()


if __name__ == '__main__':
    Rus()


# with open(r'rank.csv', 'a', encoding='utf-8') as fd:
#     list_ = [['时间', '分数', '四消', '三消', '双消', '单消']]
#     writer = csv.writer(fd)
#     writer.writerows(list_)

