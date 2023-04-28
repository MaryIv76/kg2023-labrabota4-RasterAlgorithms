from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button
import time


def step_by_step(x, k, b, steps):
    begin = time.time()

    x = int(round(x))
    steps = int(round(steps))
    x_coordinates = []
    y_coordinates = []

    for i in range(steps):
        y = int(round(k * x + b))
        x_coordinates.append(x)
        y_coordinates.append(y)
        x += 1

    end = time.time()
    print('Step by step. Time spent: {}'.format(end - begin))

    return x_coordinates, y_coordinates


def dda(x1, y1, x2, y2):
    begin = time.time()

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = float(x1)
    y = float(y1)

    x_coordinates = []
    y_coordinates = []
    x_coordinates.append(x)
    y_coordinates.append(y)

    for i in range(steps):
        x += x_inc
        y += y_inc
        x_coordinates.append(x)
        y_coordinates.append(y)

    end = time.time()
    print('DDA. Time spent: {}'.format(end - begin))

    return x_coordinates, y_coordinates


def swap(x, y):
    return y, x


def determine_octant(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if (x1 < x2) and (y1 < y2) and (dx >= dy):
        return 1
    if (x1 < x2) and (y1 < y2) and (dx < dy):
        return 2
    if (x1 > x2) and (y1 < y2) and (dx <= dy):
        return 3
    if (x1 > x2) and (y1 < y2) and (dx > dy):
        return 4
    if (x1 > x2) and (y1 > y2) and (dx >= dy):
        return 5
    if (x1 > x2) and (y1 > y2) and (dx < dy):
        return 6
    if (x1 < x2) and (y1 > y2) and (dx <= dy):
        return 7
    if (x1 < x2) and (y1 > y2) and (dx > dy):
        return 8


def preprocess_points(x1, y1, x2, y2):
    octant = determine_octant(x1, y1, x2, y2)
    if octant == 1:
        dx = x2 - x1
        dy = y2 - y1
        swap_x_y = False
        y_minus = False
    if octant == 2:
        x1, y1 = swap(x1, y1)
        x2, y2 = swap(x2, y2)
        dx = x2 - x1
        dy = y2 - y1
        swap_x_y = True
        y_minus = False
    if octant == 3:
        x1, y1 = swap(x1, y1)
        x2, y2 = swap(x2, y2)
        dx = x2 - x1
        dy = -1 * (y2 - y1)
        swap_x_y = True
        y_minus = True
    if octant == 4:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
        dx = x2 - x1
        dy = -1 * (y2 - y1)
        swap_x_y = False
        y_minus = True
    if octant == 5:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
        dx = x2 - x1
        dy = y2 - y1
        swap_x_y = False
        y_minus = False
    if octant == 6:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
        x1, y1 = swap(x1, y1)
        x2, y2 = swap(x2, y2)
        dx = x2 - x1
        dy = y2 - y1
        swap_x_y = True
        y_minus = False
    if octant == 7:
        x1, y1 = swap(x1, y1)
        x2, y2 = swap(x2, y2)
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
        dx = x2 - x1
        dy = -1 * (y2 - y1)
        swap_x_y = True
        y_minus = True
    if octant == 8:
        dx = x2 - x1
        dy = -1 * (y2 - y1)
        swap_x_y = False
        y_minus = True

    d = 2 * dy - dx
    de = 2 * dy
    dne = 2 * (dy - dx)
    return x1, y1, x2, y2, d, de, dne, swap_x_y, y_minus


# D = 2*dy – dx
# DE = 2*dy
# DNE = 2(dy – dx)
def bresenham_line(x1, y1, x2, y2):
    begin = time.time()

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    x1, y1, x2, y2, d, de, dne, swap_x_y, y_minus = preprocess_points(x1, y1, x2, y2)

    x = x1
    y = y1

    x_coordinates = []
    y_coordinates = []
    x_coordinates.append(x)
    y_coordinates.append(y)

    while x < x2:
        if d > 0:
            x += 1
            if y_minus:
                y -= 1
            else:
                y += 1
            d += dne
        else:
            x += 1
            d += de
        x_coordinates.append(x)
        y_coordinates.append(y)

    end = time.time()
    print('Bresenham line. Time spent: {}'.format(end - begin))

    if swap_x_y:
        return y_coordinates, x_coordinates
    else:
        return x_coordinates, y_coordinates


def add_bresenham_circle_coordinates(x_coordinates, y_coordinates, x0, y0):
    x_all_coordinates = []
    y_all_coordinates = []

    for i in range(len(x_coordinates)):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(x + x0)
        y_all_coordinates.append(y + y0)
    for i in reversed(range(len(x_coordinates))):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(y + x0)
        y_all_coordinates.append(x + y0)
    for i in range(len(x_coordinates)):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(y + x0)
        y_all_coordinates.append(-x + y0)
    for i in reversed(range(len(x_coordinates))):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(x + x0)
        y_all_coordinates.append(-y + y0)
    for i in range(len(x_coordinates)):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(-x + x0)
        y_all_coordinates.append(-y + y0)
    for i in reversed(range(len(x_coordinates))):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(-y + x0)
        y_all_coordinates.append(-x + y0)
    for i in range(len(x_coordinates)):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(-y + x0)
        y_all_coordinates.append(x + y0)
    for i in reversed(range(len(x_coordinates))):
        x = x_coordinates[i]
        y = y_coordinates[i]
        x_all_coordinates.append(-x + x0)
        y_all_coordinates.append(y + y0)
    return x_all_coordinates, y_all_coordinates


def bresenham_circle(x0, y0, r):
    begin = time.time()

    x0 = int(round(x0))
    y0 = int(round(y0))
    r = int(round(r))

    x = 0
    y = r
    e = 3 - 2 * r

    x_coordinates = []
    y_coordinates = []
    x_coordinates.append(x)
    y_coordinates.append(y)

    while x < y:
        if e >= 0:
            e += 4 * (x - y) + 10
            x += 1
            y -= 1
        else:
            e += 4 * x + 6
            x += 1
        x_coordinates.append(x)
        y_coordinates.append(y)

    x_coordinates, y_coordinates = add_bresenham_circle_coordinates(x_coordinates, y_coordinates, x0, y0)

    end = time.time()
    print('Bresenham circle. Time spent: {}'.format(end - begin))

    return x_coordinates, y_coordinates


def step_by_step_fields_valid():
    valid = True
    if tb_x_step_by_step.text == "":
        ax_x_step_by_step.spines[:].set_color("red")
        valid = False
    else:
        ax_x_step_by_step.spines[:].set_color("black")
    if tb_k_step_by_step.text == "":
        ax_k_step_by_step.spines[:].set_color("red")
        valid = False
    else:
        ax_k_step_by_step.spines[:].set_color("black")
    if tb_b_step_by_step.text == "":
        ax_b_step_by_step.spines[:].set_color("red")
        valid = False
    else:
        ax_b_step_by_step.spines[:].set_color("black")
    if tb_steps_step_by_step.text == "" or int(tb_steps_step_by_step.text) <= 0:
        ax_steps_step_by_step.spines[:].set_color("red")
        valid = False
    else:
        ax_steps_step_by_step.spines[:].set_color("black")
    return valid


def start_step_by_step(init):
    if not step_by_step_fields_valid():
        return

    x = int(tb_x_step_by_step.text)
    k = float(tb_k_step_by_step.text)
    b = float(tb_b_step_by_step.text)
    steps = int(tb_steps_step_by_step.text)

    x_step_by_step, y_step_by_step = step_by_step(x, k, b, steps)

    plt.subplot(2, 4, 1)
    plt.cla()
    plt.plot(x_step_by_step, y_step_by_step, marker="o", markersize=2, markerfacecolor="green")
    plt.title("Пошаговый алгоритм")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    if not init:
        plt.show()


def on_btn_update_step_by_step_click(event):
    start_step_by_step(False)


def dda_fields_valid():
    valid = True
    if tb_x1_dda.text == "":
        ax_x1_dda.spines[:].set_color("red")
        valid = False
    else:
        ax_x1_dda.spines[:].set_color("black")
    if tb_y1_dda.text == "":
        ax_y1_dda.spines[:].set_color("red")
        valid = False
    else:
        ax_y1_dda.spines[:].set_color("black")
    if tb_x2_dda.text == "":
        ax_x2_dda.spines[:].set_color("red")
        valid = False
    else:
        ax_x2_dda.spines[:].set_color("black")
    if tb_y2_dda.text == "":
        ax_y2_dda.spines[:].set_color("red")
        valid = False
    else:
        ax_y2_dda.spines[:].set_color("black")
    return valid


def start_dda(init):
    if not dda_fields_valid():
        return

    x1 = int(tb_x1_dda.text)
    y1 = int(tb_y1_dda.text)
    x2 = int(tb_x2_dda.text)
    y2 = int(tb_y2_dda.text)

    x_dda, y_dda = dda(x1, y1, x2, y2)

    plt.subplot(2, 4, 2)
    plt.cla()
    plt.plot(x_dda, y_dda, marker="o", markersize=2, markerfacecolor="green")
    plt.title("ЦДА")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    if not init:
        plt.show()


def on_btn_update_dda_click(event):
    start_dda(False)


def bresenham_line_fields_valid():
    valid = True
    if tb_x1_bresenham_line.text == "":
        ax_x1_bresenham_line.spines[:].set_color("red")
        valid = False
    else:
        ax_x1_bresenham_line.spines[:].set_color("black")
    if tb_y1_bresenham_line.text == "":
        ax_y1_bresenham_line.spines[:].set_color("red")
        valid = False
    else:
        ax_y1_bresenham_line.spines[:].set_color("black")
    if tb_x2_bresenham_line.text == "":
        ax_x2_bresenham_line.spines[:].set_color("red")
        valid = False
    else:
        ax_x2_bresenham_line.spines[:].set_color("black")
    if tb_y2_bresenham_line.text == "":
        ax_y2_bresenham_line.spines[:].set_color("red")
        valid = False
    else:
        ax_y2_bresenham_line.spines[:].set_color("black")
    return valid


def start_bresenham_line(init):
    if not bresenham_line_fields_valid():
        return

    x1 = int(tb_x1_bresenham_line.text)
    y1 = int(tb_y1_bresenham_line.text)
    x2 = int(tb_x2_bresenham_line.text)
    y2 = int(tb_y2_bresenham_line.text)

    x_bresenham_line, y_bresenham_line = bresenham_line(x1, y1, x2, y2)

    plt.subplot(2, 4, 3)
    plt.cla()
    plt.plot(x_bresenham_line, y_bresenham_line, marker="o", markersize=2, markerfacecolor="green")
    plt.title("Брезенхем")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    if not init:
        plt.show()


def on_btn_update_bresenham_line_click(event):
    start_bresenham_line(False)


def bresenham_circle_fields_valid():
    valid = True
    if tb_x0_bresenham_circle.text == "":
        ax_x0_bresenham_circle.spines[:].set_color("red")
        valid = False
    else:
        ax_x0_bresenham_circle.spines[:].set_color("black")
    if tb_y0_bresenham_circle.text == "":
        ax_y0_bresenham_circle.spines[:].set_color("red")
        valid = False
    else:
        ax_y0_bresenham_circle.spines[:].set_color("black")
    if tb_r_bresenham_circle.text == "" or int(tb_r_bresenham_circle.text) <= 0:
        ax_r_bresenham_circle.spines[:].set_color("red")
        valid = False
    else:
        ax_r_bresenham_circle.spines[:].set_color("black")
    return valid


def start_bresenham_circle(init):
    if not bresenham_circle_fields_valid():
        return

    x0 = int(tb_x0_bresenham_circle.text)
    y0 = int(tb_y0_bresenham_circle.text)
    r = int(tb_r_bresenham_circle.text)

    x_bresenham_circle, y_bresenham_circle = bresenham_circle(x0, y0, r)

    plt.subplot(2, 4, 4)
    plt.cla()
    plt.plot(x_bresenham_circle, y_bresenham_circle, marker="o", markersize=2, markerfacecolor="green")
    plt.title("Брезенхем для окружности")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    if not init:
        plt.show()


def on_btn_update_bresenham_circle_click(event):
    start_bresenham_circle(False)


plt.figure(figsize=(12, 5))

text_box = plt.axes([0.15, 0.4, 0.1, 0.04])
ax_x_step_by_step = plt.gca()
tb_x_step_by_step = TextBox(text_box, "x: ")
tb_x_step_by_step.set_val("-10")

text_box = plt.axes([0.15, 0.35, 0.1, 0.04])
ax_k_step_by_step = plt.gca()
tb_k_step_by_step = TextBox(text_box, "k: ")
tb_k_step_by_step.set_val("10000")

text_box = plt.axes([0.15, 0.3, 0.1, 0.04])
ax_b_step_by_step = plt.gca()
tb_b_step_by_step = TextBox(text_box, "b: ")
tb_b_step_by_step.set_val("99995")

text_box = plt.axes([0.15, 0.25, 0.1, 0.04])
ax_steps_step_by_step = plt.gca()
tb_steps_step_by_step = TextBox(text_box, "steps: ")
tb_steps_step_by_step.set_val("100")

axes_button_step_by_step = plt.axes([0.15, 0.15, 0.1, 0.04])
btn_update_step_by_step = Button(axes_button_step_by_step, 'Обновить')
btn_update_step_by_step.on_clicked(on_btn_update_step_by_step_click)

text_box = plt.axes([0.36, 0.4, 0.1, 0.04])
ax_x1_dda = plt.gca()
tb_x1_dda = TextBox(text_box, "x1: ")
tb_x1_dda.set_val("-10")

text_box = plt.axes([0.36, 0.35, 0.1, 0.04])
ax_y1_dda = plt.gca()
tb_y1_dda = TextBox(text_box, "y1: ")
tb_y1_dda.set_val("-5")

text_box = plt.axes([0.36, 0.3, 0.1, 0.04])
ax_x2_dda = plt.gca()
tb_x2_dda = TextBox(text_box, "x2: ")
tb_x2_dda.set_val("90")

text_box = plt.axes([0.36, 0.25, 0.1, 0.04])
ax_y2_dda = plt.gca()
tb_y2_dda = TextBox(text_box, "y2: ")
tb_y2_dda.set_val("999995")

axes_button_dda = plt.axes([0.36, 0.15, 0.1, 0.04])
btn_update_dda = Button(axes_button_dda, 'Обновить')
btn_update_dda.on_clicked(on_btn_update_dda_click)

text_box = plt.axes([0.57, 0.4, 0.1, 0.04])
ax_x1_bresenham_line = plt.gca()
tb_x1_bresenham_line = TextBox(text_box, "x1: ")
tb_x1_bresenham_line.set_val("-10")

text_box = plt.axes([0.57, 0.35, 0.1, 0.04])
ax_y1_bresenham_line = plt.gca()
tb_y1_bresenham_line = TextBox(text_box, "y1: ")
tb_y1_bresenham_line.set_val("-5")

text_box = plt.axes([0.57, 0.3, 0.1, 0.04])
ax_x2_bresenham_line = plt.gca()
tb_x2_bresenham_line = TextBox(text_box, "x2: ")
tb_x2_bresenham_line.set_val("90")

text_box = plt.axes([0.57, 0.25, 0.1, 0.04])
ax_y2_bresenham_line = plt.gca()
tb_y2_bresenham_line = TextBox(text_box, "y2: ")
tb_y2_bresenham_line.set_val("999995")

axes_button_bresenham_line = plt.axes([0.57, 0.15, 0.1, 0.04])
btn_update_bresenham_line = Button(axes_button_bresenham_line, 'Обновить')
btn_update_bresenham_line.on_clicked(on_btn_update_bresenham_line_click)

text_box = plt.axes([0.77, 0.4, 0.1, 0.04])
ax_x0_bresenham_circle = plt.gca()
tb_x0_bresenham_circle = TextBox(text_box, "x0: ")
tb_x0_bresenham_circle.set_val("100")

text_box = plt.axes([0.77, 0.35, 0.1, 0.04])
ax_y0_bresenham_circle = plt.gca()
tb_y0_bresenham_circle = TextBox(text_box, "y0: ")
tb_y0_bresenham_circle.set_val("0")

text_box = plt.axes([0.77, 0.3, 0.1, 0.04])
ax_r_bresenham_circle = plt.gca()
tb_r_bresenham_circle = TextBox(text_box, "r: ")
tb_r_bresenham_circle.set_val("1000000")

axes_button_bresenham_circle = plt.axes([0.77, 0.15, 0.1, 0.04])
btn_update_bresenham_circle = Button(axes_button_bresenham_circle, 'Обновить')
btn_update_bresenham_circle.on_clicked(on_btn_update_bresenham_circle_click)

start_step_by_step(True)
start_dda(True)
start_bresenham_line(True)
start_bresenham_circle(True)

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()

