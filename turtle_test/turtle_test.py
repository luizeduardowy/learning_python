import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.pensize(2)
t.speed(5)

def move_t_up():
    t.speed(10)
    t.speed(5)
    t.forward(25)

def move_t_down():
    t.speed(10)
    t.speed(5)
    t.backward(25)

def move_t_right():
    t.speed(10)
    t.right(15)
    t.speed(5)

def move_t_left():
    t.speed(10)
    t.left(15)
    t.speed(5)

def clear_screen():
    t.clear()

def pen():
    if t.isdown():
        t.penup()
    else:
        t.pendown()

screen.onkey(move_t_down, 'Down')
screen.onkey(move_t_up, 'Up')
screen.onkey(move_t_left, 'Left')
screen.onkey(move_t_right, 'Right')
screen.onkey(clear_screen, 'c')
screen.onkey(pen, 'p')

screen.delay(25)
screen.listen()
screen.mainloop()
