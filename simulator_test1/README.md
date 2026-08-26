# Object Gravity Simulator

This program simulates any amount of objects, from 0 to 36, moving in a two-dimensional terminal grid. Each object has a unique identifier, position, mass, and velocity. The objects attract one another using a simplified gravity calculation, while friction limits their movement.

The simulation displays the objects as characters in the terminal. IDs use digits and lowercase letters, so the objects are named from `object0` through `objectr`. If two or more objects occupy the same position, that position is displayed as `O`.

## Requirements

- Python 3
- A terminal at least 55 characters wide
- A terminal that supports screen clearing

## How to Run

Open PowerShell in the project root:

```powershell
cd "C:\Users\luizeduardo\Desktop\Aulas_Python\learning_python"
```

Run the simulator with Python:

```powershell
py .\simulator_test1\sim_test1.py
```

If the project virtual environment is enabled, you can also run:

```powershell
.\.venv\Scripts\python.exe .\simulator_test1\sim_test1.py
```

You can run the command from inside the simulator folder as well:

```powershell
cd .\simulator_test1
py .\sim_test1.py
```

## Controls

The simulation runs continuously. Press `Ctrl+C` to stop it.

## Configuration

The main settings are at the top of `sim_test1.py`:

- `object_count`: number of simulated objects; the maximum is 36
- `fps`: approximate number of frames displayed per second
- `x_frame_size`: terminal grid width
- `y_frame_size`: terminal grid height
- `max_speed`: maximum speed in either direction
- `friction`: amount of velocity reduction each update
- `gravitational_constant`: strength of the simulated gravity

The object positions, masses, and initial velocities are generated randomly each time the program starts, so every run can behave differently.

## How It Works

For each frame, the program:

1. Clears the terminal.
2. Prints the current frame number.
3. Draws the objects on the grid.
4. Calculates the gravitational effect between every pair of objects.
5. Applies friction and speed limits.
6. Moves the objects according to their velocities.

Objects wrap around the edges of the grid. An object leaving one side reappears on the opposite side.

## Mathematical Model

The movement is based on Newton's law of universal gravitation. Each object attracts every other object. The attraction is calculated pair by pair, so this is an N-body simulation.

### 1. Relative position

For an object at `(x1, y1)` and another object at `(x2, y2)`, the code calculates the relative position:

```text
dx = x2 - x1
dy = y2 - y1
```

The function `distance()` also calculates the distance between the objects using the Pythagorean theorem:

```text
r = sqrt(dx^2 + dy^2)
```

Here, `dx` and `dy` are the components of the direction vector and `r` is the distance between the objects.

### 2. Newton's gravitational law

The scalar form of Newton's law is:

```text
F = G * (m1 * m2) / r^2
```

where:

- `F` is the gravitational force
- `G` is `gravitational_constant`
- `m1` and `m2` are the object masses
- `r` is the distance between the objects

The program needs the force's horizontal and vertical components, not only its total magnitude. The direction vector is normalized by dividing it by `r`, which results in:

```text
Fx = G * m1 * m2 * dx / r^3
Fy = G * m1 * m2 * dy / r^3
```

This is equivalent to calculating the force magnitude and then splitting it into the `x` and `y` directions.

### 3. Converting force into acceleration

Newton's second law says:

```text
a = F / m
```

The code divides each force component by the mass of the current object (`m1`). Therefore, the acceleration added to that object is effectively:

```text
ax = G * m2 * dx / r^3
ay = G * m2 * dy / r^3
```

The other object's mass affects the acceleration, while the current object's mass cancels out during the division.

### 4. Minimum distance protection

When `r` is less than `0.75`, the code sets the force to zero:

```python
if dist[2] >= 0.75:
	# calculate gravity
else:
	force[i] = 0
```

This prevents the force from becoming extremely large, or from causing a division-by-zero error when two objects share the same position.

### 5. Friction

After gravitational acceleration is applied, the code reduces the velocity:

```text
vx = vx - (vx * friction)
vy = vy - (vy * friction)
```

This is equivalent to:

```text
vx = vx * (1 - friction)
vy = vy * (1 - friction)
```

With the current `friction` value of `0.0025`, each gravity calculation reduces the current velocity by 0.25 percent. In the current implementation this happens once for every other object, during each frame.

### 6. Position update

After gravity and friction are applied, the object position changes according to its velocity:

```text
x = x + vx
y = y + vy
```

The program does not currently multiply this update by a time step such as `dt`. Therefore, changing `fps` changes how often updates happen, but does not automatically make the movement time-independent.

### 7. Boundary wrapping

When an object leaves the visible area, its position is moved to the opposite side:

```text
if x > frame_width - 1: x = 1
if x < 0:              x = frame_width - 1
if y > frame_height - 1: y = 1
if y < 0:                y = frame_height - 1
```

This makes the simulation behave like a toroidal space: there are no permanent walls at the edges.

### Complete update cycle

For each object, the current implementation follows this sequence:

```text
1. Wrap the object around the boundaries when necessary.
2. Limit its current velocity to max_speed.
3. For every other object, calculate dx, dy, and r.
4. Calculate the gravitational force components.
5. Convert force into acceleration.
6. Add acceleration to the object's velocity.
7. Apply friction after each pair interaction.
8. Move the object using its resulting velocity.
```

The model is useful for visualization and learning, but it is not a physically exact simulation. The small grid, random masses, simplified boundary behavior, frame-based movement, and very small gravitational constant all affect the result.
