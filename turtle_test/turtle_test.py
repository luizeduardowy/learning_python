import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.pensize(2)
t.speed(5)

def move_t_up():
    t.setheading(90)
    t.forward(25)

def move_t_down():
    t.setheading(270)
    t.forward(25)

def move_t_right():
    t.setheading(0)
    t.forward(25)

def move_t_left():
    t.setheading(180)
    t.forward(25)

screen.onkey(move_t_down, 'Down')
screen.onkey(move_t_up, 'Up')
screen.onkey(move_t_left, 'Left')
screen.onkey(move_t_right, 'Right')

screen.listen()
screen.mainloop()
