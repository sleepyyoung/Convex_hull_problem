import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

min_value = 0
max_value = 100
draw_line_lists = []


def calc_area(a, b, c):
    """
    判断三角形面积
    """
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    return x1 * y2 + x3 * y1 + x2 * y3 - x3 * y2 - x2 * y1 - x1 * y3


def rand_point_set(n, range_min=0, range_max=101):
    """
    随机生成具有 n 个点的点集
    :param range_max: 生成随机点最小值，默认 0
    :param range_min: 生成随机点最大值，默认 100
    :param n: int
    :return: list [(x1,y1)...(xn,yn)]
    """
    try:
        return list(zip([random.uniform(range_min, range_max) for _ in range(n)],
                        [random.uniform(range_min, range_max) for _ in range(n)]))
    except IndexError as e:
        print("\033[31m" + ''.join(e.args) + "\n输入范围有误！" + '\033[0m')


def border_point_up(left_point, right_point, lists, border_points):
    """
    寻找上半部分边界点
    :param left_point: tuple, 最左边的点
    :param right_point: tuple, 最右边的点
    :param lists: 所有的点集
    :param border_points: 边界点集
    :return:
    """
    draw_line_lists.append(left_point)
    draw_line_lists.append(right_point)

    area_max = 0
    max_point = ()
    for item in lists:
        if item == left_point or item == right_point:
            continue
        else:
            max_point = item if calc_area(left_point, right_point, item) > area_max else max_point
            area_max = calc_area(left_point, right_point, item) if calc_area(left_point, right_point,
                                                                             item) > area_max else area_max
    if area_max != 0:
        border_points.append(max_point)
        border_point_up(left_point, max_point, lists, border_points)
        border_point_up(max_point, right_point, lists, border_points)


def border_point_down(left_point, right_point, lists, border_points):
    """
    寻找下半部分边界点
    :param left_point: tuple, 最左边的点
    :param right_point: tuple, 最右边的点
    :param lists: 所有的点集
    :param border_points: 边界点集
    :return:
    """
    draw_line_lists.append(left_point)
    draw_line_lists.append(right_point)

    area_max = 0
    max_point = ()
    for item in lists:
        if item == left_point or item == right_point:
            continue
        else:
            max_point = item if calc_area(left_point, right_point, item) < area_max else max_point
            area_max = calc_area(left_point, right_point, item) if calc_area(left_point, right_point,
                                                                             item) < area_max else area_max
    if area_max != 0:
        border_points.append(max_point)
        border_point_down(left_point, max_point, lists, border_points)
        border_point_down(max_point, right_point, lists, border_points)


def order_border(lists):
    """
    返回顺时针的边界点集
    :param lists: 无序边界点集
    :return: list [( , )...( , )]
    """
    lists.sort()
    first_x, first_y = lists[0]  # 最左边的点
    last_x, last_y = lists[-1]  # 最右边的点
    list_border_up = []  # 上半边界
    for item in lists:
        x, y = item
        if y > max(first_y, last_y):
            list_border_up.append(item)
        if min(first_y, last_y) < y < max(first_y, last_y):
            if calc_area(lists[0], lists[-1], item) > 0:
                list_border_up.append(item)
            else:
                continue
    list_border_down = [_ for _ in lists if _ not in list_border_up]  # 下半边界
    list_end = list_border_up + list_border_down[::-1]  # 最终顺时针输出的边界点
    return list_end


def draws(list_points, list_frames, gif_name="save.gif"):
    """
    生成动态图并保存
    :param list_points: 所有点集
    :param list_frames: 帧 列表
    :param gif_name: 保存动图名称
    :return: .gif
    """
    list_all_x = []
    list_all_y = []
    for item in list_points:
        a, b = item
        list_all_x.append(a)
        list_all_y.append(b)

    fig, ax = plt.subplots()  # 生成轴和fig,  可迭代的对象
    x, y = [], []  # 用于接受后更新的数据
    line, = plt.plot([], [], color="red")  # 绘制线对象，plot返回值类型，要加逗号

    def init():
        # 初始化函数用于绘制一块干净的画布，为后续绘图做准备
        ax.set_xlim(min_value - abs(min_value * 0.1), max_value + abs(max_value * 0.1))  # 初始函数，设置绘图范围
        ax.set_ylim(min_value - abs(min_value * 0.1), max_value + abs(max_value * 0.1))
        return line

    def update(lists):
        a, b = lists
        x.append(a)
        y.append(b)
        line.set_data(x, y)
        return line

    plt.scatter(list_all_x, list_all_y)  # 绘制所有散点
    ani = animation.FuncAnimation(fig, update, frames=list_frames, init_func=init, interval=500)
    ani.save(gif_name, writer='pillow')


def show_result(list_points, list_borders):
    """
    画图
    :param list_points: 所有点集
    :param list_borders: 所有边集
    :return: picture
    """
    list_all_x = []
    list_all_y = []
    for item in list_points:
        a, b = item
        list_all_x.append(a)
        list_all_y.append(b)

    for i in range(len(list_borders)-1):
        item_1=list_borders[i]
        item_2 = list_borders[i+1]
        #  横坐标,纵坐标
        one_, oneI = item_1
        two_, twoI = item_2
        plt.plot([one_, two_], [oneI, twoI])
    plt.scatter(list_all_x, list_all_y)
    plt.show()


def main():
    """
    :return: 所有点
    """
    global min_value, max_value
    inputs = list(map(int, input().split()))
    if len(inputs) == 1:
        n = inputs[0]
        return rand_point_set(n)
    elif len(inputs) == 2:
        n, min_value = inputs[0], inputs[1]
        return rand_point_set(n, min_value)
    elif len(inputs) == 3:
        n, min_value, max_value = inputs[0], inputs[1], inputs[2]
        return rand_point_set(n, min_value, max_value)
    else:
        print("\033[31m输入数据太多,请重新输入!\033[0m")
        main()


if __name__ == "__main__":
    print("""输入规则:
最少一个最多三个
后面可以跟数字用来指定生成区间(默认[0，100])，中间用空格隔开
例如：
    输入 10   ---即为在默认区间[0，100]生成10个随机点
    输入 10 50   ---即为在区间[50,100]生成10个随机点
    输入 10 50 200   ---即为在区间[50,200]生成10个随机点
请输入:\t""")
    list_points = main()  # 所有点
    list_points.sort()
    border_points = []  # 边界点集
    border_point_up(list_points[0], list_points[-1], list_points, border_points)  # 上边界点集
    border_point_down(list_points[0], list_points[-1], list_points, border_points)  # 下边界点集
    border_points.append(list_points[0])
    border_points.append(list_points[-1])  # 将首尾两个点添加到边界点集中
    list_borders = order_border(border_points)  # 顺时针边界点
    # print(order_border(border_points))  # 顺时针输出边界点
    list_borders.append(list_borders[0])  # 顺时针边界点闭合
    show_result(list_points,list_borders)   # 显示静态结果
    draws(list_points, draw_line_lists, "process.gif")  # 绘制动态过程
    draws(list_points, list_borders, "result.gif")  # 绘制动态结果
