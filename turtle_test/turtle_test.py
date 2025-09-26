import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.pensize(2)
t.speed(5)

def move_t_up():
    t.speed(10)
    t.setheading(90)
    t.speed(5)
    t.forward(25)

def move_t_down():
    t.speed(10)
    t.setheading(270)
    t.speed(5)
    t.forward(25)

def move_t_right():
    t.speed(10)
    t.setheading(0)
    t.speed(5)
    t.forward(25)

def move_t_left():
    t.speed(10)
    t.setheading(180)
    t.speed(5)
    t.forward(25)

screen.onkey(move_t_down, 'Down')
screen.onkey(move_t_up, 'Up')
screen.onkey(move_t_left, 'Left')
screen.onkey(move_t_right, 'Right')

screen.delay(25)
screen.listen()
screen.mainloop()
