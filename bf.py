import random
import matplotlib.pyplot as plt


def is_one_side(a, b, c):
    """
    判断一个点在一条直线的左边还是右边
    判断点 C(x3,y3) 在直线 AB 的左边还是右边
                     [ 其中 A(x1,y1), B(x2,y2) ]
    计算此三阶行列式：
    | x1 y1 1 |
    | x2 y2 1 | = x1y2 + x3y1 + x2y3 - x3y2 - x2y1 - x1y3
    | x3 y3 1 |
    当上式结果为正时, C 在 AB 左侧
             为负时, C 在 AB 右侧
    :return: 如果点 C 在直线 AB 左侧，返回 True
             否则  返回 False
    """
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    number = x1 * y2 + x3 * y1 + x2 * y3 - x3 * y2 - x2 * y1 - x1 * y3
    if x1 == x2 == x3 or y1 == y2 == y3 or a == c or b == c:
        number = 0
    return number
    """
    return np.linalg.det([[x1, y1, 1],
                          [x2, y2, 1],
                          [x3, y3, 1]])
    这种方法按理说也可以，但是不知道为啥，有问题...比如：
    np.linalg.det([[1, 1, 1],
                   [2, 2, 1],
                   [3, 3, 1]])
    这种方法算这个玩意是不等于 0 的，不知道为啥...
    """


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


def combine_line(lists):
    """
    蛮力法输出边界边集
    :param lists:
    :return: list [( , )...( , )]
    """
    lists.sort()
    list_border_line = []  # 边集
    for i in lists:
        for j in lists[lists.index(i) + 1:]:
            count_left = 0
            count_right = 0
            for k in lists:
                if k == i or k == j:
                    continue
                else:
                    if is_one_side(i, j, k) > 0:
                        count_left += 1
                    if is_one_side(i, j, k) < 0:
                        count_right += 1
                    if is_one_side(i, j, k) == 0:
                        pass
            if count_right != 0 and count_left != 0:
                pass
            else:
                list_border_line.append((i, j))
    return list_border_line


def combine_point(list_border_line):
    """
    返回顺时针边界点集
    ！！！注意，这个函数和matplotlib画图完全没关系！！！
    只是为了让大家方便看到顺时针输出的点集
    不要这个函数完全没问题
    因为我用matplotlib画图是根据上一个函数直接画线的，没有用到这个点集
    :param list_border_line: 边集
    :return: list [( , )...( , )]
    """
    list_border_point = []
    for _ in list_border_line:
        a, b = _
        list_border_point.append(a)
        list_border_point.append(b)
    list_border_point = sorted(list(set(list_border_point)))  # 有序边界点
    first_x, first_y = list_border_point[0]  # 最左边的点
    last_x, last_y = list_border_point[-1]  # 最右边的点
    list_border_up = []  # 上半边界
    for item in list_border_point:
        x, y = item
        if y > max(first_y, last_y):
            list_border_up.append(item)
        if min(first_y, last_y) < y < max(first_y, last_y):
            if is_one_side(list_border_point[0], list_border_point[-1], item) > 0:
                list_border_up.append(item)
            else:
                continue
    list_border_down = [_ for _ in list_border_point if _ not in list_border_up]  # 下半边界
    list_end = list_border_up + list_border_down[::-1]  # 最终顺时针输出的边界点
    return list_end


def draw(list_all, list_border):
    """
    画图
    :param list_all: 所有点集
    :param list_border: 所有边集
    :return: picture
    """
    list_all_x = []
    list_all_y = []
    for item in list_all:
        a, b = item
        list_all_x.append(a)
        list_all_y.append(b)
    for item in list_border:
        item_1, item_2 = item
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
    inputs = list(map(int, input().split()))
    if len(inputs) == 1:
        return rand_point_set(inputs[0])
    elif len(inputs) == 2:
        return rand_point_set(inputs[0], inputs[1])
    elif len(inputs) == 3:
        return rand_point_set(inputs[0], inputs[1], inputs[2])
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
    # print(combine_point(combine_line(list_points)))  # 顺时针输出边界点
    draw(list_points, combine_line(list_points))

