def left():
    global j_loc
    if j_loc > 0:
        j_loc -= 1


def right():
    global j_loc
    if j_loc < 9:
        j_loc += 1


def top():
    global i_loc
    if i_loc > 0:
        i_loc -= 1


def button():
    global i_loc
    if i_loc < 9:
        i_loc += 1