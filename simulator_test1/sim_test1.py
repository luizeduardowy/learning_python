import random
import math
import os
import time

gravitational_constant = 6.67430e-11
object_count = 3 # Limited to 36 due to how the objects are identified
object_ids = "0123456789abcdefghijklmnopqrstuvwxyz"
fps = 30
frame = 0
x_frame_size = 55
y_frame_size = 25
max_speed = 4
friction = 0.0025
objects_list = {}
for obj_index in range(object_count):
    objects_list[f"object{object_ids[obj_index]}"] = {}

def distance(x1, y1, x2, y2):
    return [(x2 - x1), (y2 - y1), math.hypot((x2 - x1), (y2 - y1))]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_objects(objects):
    for y in range(y_frame_size):
        if all(int(obj["y"]) != y for obj in objects.values()):
            print(" ", end="")
            print()
            continue
        for x in range(x_frame_size):
            if any(int(obj["x"]) == x and int(obj["y"]) == y for obj in objects.values()):
                objs_in_xy = []
                for obj_name, obj in objects_list.items():
                    if int(obj["x"]) == x and int(obj["y"]) == y:
                        objs_in_xy.append(obj_name.removeprefix("object"))
                if len(objs_in_xy) >= 2:
                    print(f"O", end="")
                else:
                    print(f"{objs_in_xy[0]}", end="")
            else:
                print(" ", end="")
        print()

def gravity(objects):
    for obj in objects.values():
        if obj["y"] > y_frame_size - 1:
            obj["y"] = 1
        if obj["y"] < 0:
            obj["y"] = y_frame_size - 1
        if obj["x"] > x_frame_size - 1:
            obj["x"] = 1
        if obj["x"] < 0:
            obj["x"] = x_frame_size - 1
        if abs(obj["speed"]["x"]) > max_speed:
            if abs(obj["speed"]["x"]) == obj["speed"]["x"]:                            
                obj["speed"]["x"] = max_speed
            else:
                obj["speed"]["x"] = -1 * max_speed
        if abs(obj["speed"]["y"]) > max_speed:
            if abs(obj["speed"]["y"]) == obj["speed"]["y"]:
                obj["speed"]["y"] = max_speed
            else:
                obj["speed"]["y"] = -1 * max_speed

        for other_obj in objects.values():
            if obj != other_obj:
                dist = distance(obj["x"], obj["y"], other_obj["x"], other_obj["y"])
                force = [0, 0, 0]
                for i in range(3):
                    if dist[2] >= 0.75:
                        force[i] = ((obj["mass"] * other_obj["mass"]) * (dist[i] / dist[2] ** 3))
                    else:
                        force[i] = 0
                obj["speed"]["x"] += (force[0] / obj["mass"]) * gravitational_constant
                obj["speed"]["y"] += (force[1] / obj["mass"]) * gravitational_constant
                obj["speed"]["x"] -= (obj["speed"]["x"] * friction)
                obj["speed"]["y"] -= (obj["speed"]["y"] * friction)

def move_objects(objects):
    for obj in objects.values():
        obj["x"] += obj["speed"]["x"]
        obj["y"] += obj["speed"]["y"]

for object in objects_list:
    objects_list[object]["x"] = random.randint(1, x_frame_size - 1)
    objects_list[object]["y"] = random.randint(1, y_frame_size - 1)
    objects_list[object]["mass"] = random.uniform(1e7, 1e10)
    objects_list[object]["speed"] = {"x": random.uniform(1, -1) / objects_list[object]["mass"], "y": random.uniform(1, -1) / objects_list[object]["mass"]}

while True:
    time.sleep(1 / fps)
    clear_screen()
    print(f"Remember to keep the terminal at least as wide as the frame width({x_frame_size} characters)")
    print(f"Expected fps: {fps}")
    print(f"Frame {frame}")
    print("-" * x_frame_size)
    print_objects(objects_list)
    gravity(objects_list)
    move_objects(objects_list)
    print("-" * x_frame_size)
    frame += 1