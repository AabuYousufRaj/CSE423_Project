from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math


# Window dimensions
width, height = 800, 600
# Global variables
is_day = True
raindrops_list = []
raindrops_falling = False  # Track whether raindrops are falling
thunder_occurred = False
# Track if thunder occurred
bx = -100
lx = -200
cars = []
trees = []
lamps = []
num_cars = 5


# Global variables
snowflakes_list = []
snowfall_active = False  # Track whether snow is falling




def init():
    global cars, trees, lamps
    glClearColor(0.53, 0.81, 0.92, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
   
    cars = []
    for _ in range(num_cars):
        x = random.randint(0, width)
        y = random.choice([70, 130])
        direction = 1 if y == 70 else -1
        cars.append(Car(x, y, direction))
   
    # Alternating trees and lamps
    trees = []
    lamps = []
    tree_spacing = width // 9




    for i in range(8):


        x = (i + 1) * tree_spacing
       
        if i % 2 == 0:
            trees.append(tree(x-50, 145, height))  # Upper road
            lamps.append(lamp(x, 55, None))  # Lower road
        else:
            lamps.append(lamp(x-50, 145, None))  # Upper road
            trees.append(tree(x, 55, height))  # Lower road


def draw_pixel(x, y, color):
    """Draw a single pixel."""
    glColor3f(*color)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()




def draw_circle(x_center, y_center, radius, color):
    """Draw a filled circle using the Midpoint Circle Drawing Algorithm."""
    x = radius
    y = 0
    p = 1 - radius  # Midpoint circle drawing parameter


    while x >= y:
        for i in range(x_center - x, x_center + x + 1):
            draw_pixel(i, y_center + y, color)  # Top side
            draw_pixel(i, y_center - y, color)  # Bottom side
        for i in range(x_center - y, x_center + y + 1):
            draw_pixel(i, y_center + x, color)  # Right side
            draw_pixel(i, y_center - x, color)  # Left side
        y += 1
        if p <= 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1
           
           
def draw_window(x, y, w, h, color):
    """Fill a rectangle using horizontal lines."""
    for i in range(h):
        draw_line(x, y + i, x + w, y + i, color)








def draw_line(x1, y1, x2, y2, color):
    """Draw a line using the Midpoint Line Drawing Algorithm."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
















    while True:
        draw_pixel(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy








def draw_building(x, y, w, h, color, window_color):
    """Draw a well-shaped building with a 3D side effect and windows."""
    depth = 40  # Depth for the 3D effect
    for px in range(x, x + w):
        for py in range(y, y + h):
            draw_pixel(px, py, color)








    rows = 4
    cols = 3
    window_w = w // cols
    window_h = h // (rows + 1)
    for i in range(rows):
        for j in range(cols):
            wx = x + j * window_w + window_w // 6
            wy = y + (i + 1) * window_h + window_h // 6
            if wx + window_w // 2 <= x + w and wy + window_h // 2 <= y + h:
                draw_window(wx, wy, window_w // 2, window_h // 2, window_color)








    for px in range(x + w, x + w + depth):
        for py in range(y, y + h):
            draw_pixel(px, py, (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7))








    for i in range(rows):
        for j in range(2):
            wx = x + w + j * (window_w // 2) + (window_w // 6)
            wy = y + (i + 1) * window_h + window_h // 6
            if wx + (window_w // 3) <= x + w + depth and wy + (window_h // 2) <= y + h:
                draw_window(wx, wy, window_w // 3, window_h // 2, window_color)








def generate_raindrop():
    """Generate a single raindrop at a random position at the top."""
    x = random.randint(0, width)  # Random horizontal position
    y = random.randint(height, height + 100)  # Random vertical starting position within a range above the screen
    raindrops_list.append([x, y])


def update_raindrops():
    """Update raindrop positions to animate falling."""
    global raindrops_list
    if raindrops_falling:
        for drop in raindrops_list:
            drop[1] -= 5  # Speed of the raindrops
            if drop[1] < 0:  # Reset the raindrop position when it moves off screen
                drop[1] = height


def draw_rain():
    """Draw the falling raindrops as small lines."""
    for drop in raindrops_list:
        draw_line(drop[0], drop[1], drop[0], drop[1] - 15, (1.0, 1.0, 1.0))  # White raindrops




def generate_thunder():
    """Simulate thunder by flashing a bright light across the screen."""
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Bright white to simulate lightning
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()
    time.sleep(0.1)  # Flash duration
    glClearColor(0.53, 0.81, 0.92, 1.0)  # Reset to day color (sky blue)
    glClear(GL_COLOR_BUFFER_BIT)




def draw_stars():
    """Draw random stars in the sky during the night."""
    num_stars = 1000  # Increased number of stars
    for _ in range(num_stars):
        x = random.randint(0, width)  # Random x position
        y = random.randint(height // 2, height)  # Random y position (upper half of the screen)




def draw_stars():
    num_stars = 1000  # Increased number of stars
    for _ in range(num_stars):
        x = random.randint(0, width)  # Random x position
        y = random.randint(height // 2, height) # Random y-coordinate








        # Avoid drawing stars where the buildings are
        if not (100 <= x <= 180 and 200 <= y <= 320):  # Building 1 area
            if not (300 <= x <= 400 and 200 <= y <= 340):  # Building 2 area
                if not (550 <= x <= 630 and 200 <= y <= 360):  # Building 3 area






                    # Avoid drawing stars in the hill areas
                    # Define the hill area using the coordinates of the hills
                    if not (x >= 50 and x <= 250 and y >= 300 and y <= 300):  
                         if not (x >= 0 and x <= 800 and y >= 300 and y <= 400):  
                              if not (x >= 0 and x <= 800 and y >= 300 and y <= 400):
                                   draw_pixel(x, y, (1.0, 1.0, 1.0))
                                 
   
def plot_circle_points(cx, cy, x, y):
    """Plot symmetric points of the circle."""
    glBegin(GL_POINTS)
    glVertex2f(cx + x, cy + y)
    glVertex2f(cx - x, cy + y)
    glVertex2f(cx + x, cy - y)
    glVertex2f(cx - x, cy - y)
    glVertex2f(cx + y, cy + x)
    glVertex2f(cx - y, cy + x)
    glVertex2f(cx + y, cy - x)
    glVertex2f(cx - y, cy - x)
    glEnd()
















def fill_circle_with_midpoint(cx, cy, radius):
    """Fill a circle using the midpoint circle drawing algorithm."""
    glBegin(GL_POINTS)
    for y in range(-radius, radius + 1):
        span = int(math.sqrt(radius**2 - y**2))  # Calculate the span using the circle equation
        for x in range(-span, span + 1):
            glVertex2f(cx + x, cy + y)  # Fill all points in the horizontal line
    glEnd()








def cloud_circle(rx, ry, cx, cy):
    """Draw and fill an ellipse for a cloud component using midpoint circle drawing algorithm."""
    steps = 100  # Higher value = smoother ellipse
    for angle in range(0, 360, steps):
        rad = math.radians(angle)
        fill_circle_with_midpoint(cx + int(rx * math.cos(rad)), cy + int(ry * math.sin(rad)), min(rx, ry))








def small_clouds():
    global bx
    glPushMatrix()
    glTranslatef(bx, 0, 0)  # Translate clouds horizontally by bx
















    # Change cloud color to gray when it starts raining
    if raindrops_falling:
        glColor3f(0.5, 0.5, 0.5)  # Set clouds to gray
    else:
        glColor3f(1.0, 1.0, 1.0)  # Keep clouds white during the day








    # Draw the small clouds
    cloud_circle(15, 15, 132, 465)
    cloud_circle(7, 7, 127, 452)
    cloud_circle(10, 10, 142, 455)
    cloud_circle(14, 14, 158, 463)
    cloud_circle(14, 14, 143, 477)
    cloud_circle(11, 11, 122, 477)
    cloud_circle(15, 15, 114, 464)








   # Additional small clouds
    cloud_circle(20, 25, 360, 480)
    cloud_circle(15, 15, 343, 480)
    cloud_circle(13, 13, 338, 465)
    cloud_circle(13, 15, 380, 482)
    cloud_circle(10, 10, 380, 465)
    glPopMatrix()
    # Move the small clouds horizontally
    bx += 1
    if bx > width:  # Reset cloud position when it moves off-screen
        bx = random.randint(-300, -150)  # Set a new random position to the left of the screen




def large_clouds():
    global lx
    glPushMatrix()
    glTranslatef(lx, 0, 0)  # Translate clouds horizontally by lx


    # Change cloud color to gray when it starts raining
    if raindrops_falling:
        glColor3f(0.5, 0.5, 0.5)  # Set clouds to gray
    else:
        glColor3f(1.0, 1.0, 1.0)  # Keep clouds white during the day
    # 1st large cloud
    cloud_circle(15, 15, 187, 532)
    cloud_circle(13, 13, 210, 531)
    cloud_circle(13, 13, 222, 537)
    cloud_circle(12, 12, 212, 550)
    cloud_circle(16, 16, 194, 553)
    cloud_circle(13, 13, 169, 547)
    cloud_circle(11, 11, 166, 532)






    # 2nd large cloud
    cloud_circle(14, 14, 390, 570)
    cloud_circle(8, 8, 394, 560)
    cloud_circle(9, 9, 410, 562)
    cloud_circle(8, 8, 419, 574)
    cloud_circle(16, 16, 418, 587)
    cloud_circle(14, 14, 390, 590)
    cloud_circle(14, 14, 380, 580)








    glPopMatrix()
    # Move the large clouds horizontally
    lx += 1
    if lx > width:  # Reset cloud position when it moves off-screen
        lx = random.randint(-350, -250)  # Set a new random position to the left of the screen
def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    """Draw a triangle using the Midpoint Line Drawing Algorithm and fill its area."""
    draw_line(x1, y1, x2, y2, color)
    draw_line(x2, y2, x3, y3, color)
    draw_line(x3, y3, x1, y1, color)
   
    # Filling the area inside the triangle
    fill_triangle(x1, y1, x2, y2, x3, y3, color)
   
def draw_river():
        draw_triangle(0,300, width,400, width,300,(0.0, 0.3, 0.6 ))
       
def fill_triangle(x1, y1, x2, y2, x3, y3, color):
    """Fill the area inside the triangle using scanline fill or a similar algorithm."""
    # Sort the points by y-coordinates to find the top and bottom edges
    vertices = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]
   
    # Find the left and right edges of the triangle
    for y in range(int(y1), int(y3)):
        # Find the intersections of the scanline with the triangle edges
        if y < y2:
            x_left = interpolate(x1, y1, x2, y2, y)
            x_right = interpolate(x1, y1, x3, y3, y)
        else:
            x_left = interpolate(x2, y2, x3, y3, y)
            x_right = interpolate(x1, y1, x3, y3, y)
       
        # Draw a horizontal line between the left and right edges of the triangle
        draw_line(int(x_left), y, int(x_right), y, color)


def interpolate(x1, y1, x2, y2, y):
    """Interpolate the x-coordinate for a given y using linear interpolation."""
    return x1 + (x2 - x1) * (y - y1) / (y2 - y1)


def draw_hills():
    """Draw hills as triangles behind the buildings and fill the area between them."""
    hill_color = (0.439, 0.502, 0.565)  
   
    # Left hill (triangle)
    draw_triangle(50,300, 150, 400, 250, 300, hill_color)
    # Middle hill (triangle)
    draw_triangle(251, 300, 350, 450, 450, 300, hill_color)


    # Right hill (triangle)
    draw_triangle(451,300, 555, 450, 651, 300, hill_color)
   
def draw_fields():
    """Draw green fields behind the buildings using midpoint line algorithm."""
    field_color = (0.2, 0.8, 0.2)  # Bright green for fields
    for y in range(200, 300, 2):  # Gradient effect using horizontal lines
        draw_line(0, y, width, y, field_color)


def generate_snowflake():
    """Generate a single snowflake at a random position at the top."""
    x = random.randint(0, width)  # Random horizontal position
    y = random.randint(height, height + 100)  # Random vertical starting position above the screen
    snowflakes_list.append([x, y])  # Add to snowflake list
   
def update_snowflakes():
    """Update snowflake positions to animate falling."""
    global snowflakes_list
    if snowfall_active:
        for flake in snowflakes_list:
            flake[1] -= 2  # Speed of snowflakes (slower than rain)
            if flake[1] < 0:  # Reset snowflake position when it moves off-screen
                flake[1] = height
def draw_snow():
    """Draw the falling snowflakes as small circles."""
    for flake in snowflakes_list:
        draw_circle(flake[0], flake[1], 3, (1.0, 1.0, 1.0))  # White snowflakes with radius 3


def draw_road():
    # Draw main road
    road_color = (0.3, 0.3, 0.3)
    for y in range(50, 150):
        draw_line(0, y, width, y, road_color)


    # Draw road divider lines
    divider_color = (1.0, 1.0, 1.0)
    stripe_length = 30
    gap_length = 20
    y = 100
    for x in range(0, width, stripe_length + gap_length):
        draw_line(x, y, x + stripe_length, y, divider_color)


    # Draw traffic signal box at the right corner
    draw_traffic_signal()


def draw_traffic_signal():
    # Position the signal box at the right corner of the road
    box_x_min = width - 70
    box_y_min = 150
    box_x_max = width - 30
    box_y_max = 280




    # Draw signal box with a border
    outer_color = (0.1, 0.1, 0.1)  # Darker gray for the border
    inner_color = (0.2, 0.2, 0.2)  # Lighter gray for the box itself
    draw_filled_rectangle(box_x_min - 2, box_y_min - 2, box_x_max + 2, box_y_max + 2, outer_color)
    draw_filled_rectangle(box_x_min, box_y_min, box_x_max, box_y_max, inner_color)




    # Add screws at the corners
    screw_color = (0.6, 0.6, 0.6)
    screw_radius = 2
    screws = [
        (box_x_min + 2, box_y_min + 2),
        (box_x_max - 2, box_y_min + 2),
        (box_x_min + 2, box_y_max - 2),
        (box_x_max - 2, box_y_max - 2),
    ]
    for screw_x, screw_y in screws:
        draw_filled_circle(screw_x, screw_y, screw_radius, screw_color)




    # Calculate positions for the lights
    red_light_y = box_y_max - 20
    yellow_light_y = red_light_y - 35
    green_light_y = yellow_light_y - 35
    light_x = (box_x_min + box_x_max) // 2




    # Draw compartments for each light
    compartment_color = (0.15, 0.15, 0.15)
    draw_filled_rectangle(box_x_min + 2, red_light_y - 15, box_x_max - 2, red_light_y + 15, compartment_color)
    draw_filled_rectangle(box_x_min + 2, yellow_light_y - 15, box_x_max - 2, yellow_light_y + 15, compartment_color)
    draw_filled_rectangle(box_x_min + 2, green_light_y - 15, box_x_max - 2, green_light_y + 15, compartment_color)




    # Draw the lights with glow effect
    glow_radius = 15
    def draw_glowing_light(cx, cy, light_color, active):
        if active:
            glow_color = tuple(min(c + 0.5, 1.0) for c in light_color)  # Lighter color for glow
            draw_filled_circle(cx, cy, glow_radius, glow_color)
        draw_filled_circle(cx, cy, 10, light_color if active else (0.5, 0.5, 0.5))




    # Draw the red, yellow, and green lights
    draw_glowing_light(light_x, red_light_y, RED, current_color == RED)
    draw_glowing_light(light_x, yellow_light_y, YELLOW, current_color == YELLOW)
    draw_glowing_light(light_x, green_light_y, GREEN, current_color == GREEN)


class tree:
    def __init__(self, base_x, base_y, display_height):
        self.base_x = base_x
        self.base_y = base_y
        self.scale_factor = display_height / 10
        self.trunk_height = int(self.scale_factor * 1.2)
        self.trunk_width = int(self.scale_factor * 0.1)
        self.leaf_radius = int(self.scale_factor * 0.2)


    def draw(self):
        # Draw trunk
        glColor3f(0.4, 0.2, 0.1)
        left_x = self.base_x - self.trunk_width // 2
        right_x = self.base_x + self.trunk_width // 2
        for x in range(left_x, right_x + 1):
            draw_line(x, self.base_y, x, self.base_y + self.trunk_height, (0.4, 0.2, 0.1))






        # Draw leaves
        leaf_centers = [
            (self.base_x, self.base_y + self.trunk_height),
            (self.base_x - int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x + int(self.leaf_radius * 1.2), self.base_y + self.trunk_height + int(self.leaf_radius * 0.8)),
            (self.base_x, self.base_y + self.trunk_height + int(self.leaf_radius * 1.6))
        ]
       
        for x_center, y_center in leaf_centers:
            draw_circle(x_center, y_center, self.leaf_radius, (0.2, 0.6, 0.2))


signal_state=True


class Car:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = random.randint(2, 5)
        self.stopped = False




    def draw(self):
        # Adjust drawing for upper road (car in front of trees) and lower road (car behind trees)
        if self.y == 130:  # Upper road
            draw_priority = "front"  # Car is in front of trees
        elif self.y == 70:  # Lower road
            draw_priority = "back"  # Car is behind trees
        # Define the points of the car's body based on its direction
        if self.direction == 1:  # Right-facing car
            points = [
                (self.x, self.y),
                (self.x + 40, self.y),
                (self.x + 50, self.y + 15),
                (self.x + 40, self.y + 30),
                (self.x - 10, self.y + 30),
                (self.x - 10, self.y)
            ]
        else:  # Left-facing car
            points = [
                (self.x, self.y),
                (self.x - 40, self.y),
                (self.x - 50, self.y + 15),
                (self.x - 40, self.y + 30),
                (self.x + 10, self.y + 30),
                (self.x + 10, self.y)
            ]
        # Draw car body with adjusted fill color
        body_color = (1.0, 0.0, 0.0) if self.direction == 1 else (0.0, 0.0, 1.0)
        for y in range(self.y, self.y + 30):
            if self.direction == 1:  # Right-facing
                draw_line(self.x - 10, y, self.x + 40 + (10 if y < self.y + 15 else 0), y, body_color)
            else:  # Left-facing
                draw_line(self.x + 10, y, self.x - 40 - (10 if y < self.y + 15 else 0), y, body_color)


        # Draw car outline
        for i in range(len(points)):
            draw_line(points[i][0], points[i][1],
                    points[(i + 1) % len(points)][0],
                    points[(i + 1) % len(points)][1],
                    (0.3, 0.3, 0.3))  # Outline color


        # Draw wheels
        wheel_radius = 5
        if self.direction == 1:
            wheel_positions = [(self.x, self.y), (self.x + 30, self.y)]
        else:
            wheel_positions = [(self.x, self.y), (self.x - 30, self.y)]


        for wx, wy in wheel_positions:
            draw_circle(wx, wy, wheel_radius, (0.1, 0.1, 0.1))  # Black wheels
           
    def update(self):
        if signal_state:  # Green light
            if self.stopped:
                self.stopped = False  # Reset stopped state
                self.speed = random.randint(2, 5)  # Restore car speed
            self.x += self.speed * self.direction
        else:  # Red light
            self.stopped = True
        # Reset position when the car goes off screen
        if self.direction == 1 and self.x > width + 50:
            self.x = -50
        elif self.direction == -1 and self.x < -50:
            self.x = width + 50
class lamp:
    def __init__(self, x, y, ignore):
        self.x = x
        self.y = y
        self.height = 80  # Height of the lamp stand


    def draw(self):
        # Draw stand
        glColor3f(0.5, 0.5, 0.5)
        for offset in range(-3, 4):  # Thickness of the stand
            draw_line(self.x + offset, self.y, self.x + offset, self.y + self.height, (0.5, 0.5, 0.5))


        # Lamp head and connecting line
        if not is_day:  # Light color when it's night
            bulb_color = (1.0, 1.0, 0.8)
        else:
            bulb_color = (0.7, 0.7, 0.6)
           
        for side in [-1, 1]:  # Two lamp heads, one on each side
            head_x = self.x + (20 * side)
            head_y = self.y + self.height - 10


            # Draw hood (outer circle)
            draw_circle(head_x, head_y, 10, (0.2, 0.2, 0.2))
            # Draw bulb (inner circle)
            draw_circle(head_x, head_y - 3, 5, bulb_color)


            # Add connecting line from bulb to stand
            draw_line(self.x, self.y + self.height, head_x, head_y, (0.5, 0.5, 0.5))


# RGB values for the lights
RED = (1.0, 0.0, 0.0)
YELLOW = (1.0, 1.0, 0.0)
GREEN = (0.0, 1.0, 0.0)


current_color = GREEN  # Initially the light is red


# Draw filled rectangle (signal box)
def draw_filled_rectangle(x_min, y_min, x_max, y_max, color):
    glColor3f(*color)  # Set the color
    glBegin(GL_POINTS)
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            glVertex2i(x, y)  # Plot each point within the bounds
    glEnd()


# Draw filled circle (signal lights)
def draw_filled_circle(cx, cy, radius, color):
    glColor3f(*color)  # Set the color
    glBegin(GL_POINTS)
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx)**2 + (y - cy)**2 <= radius**2:  # Check if point is inside the circle
                glVertex2i(x, y)  # Plot the point
    glEnd()








# Draw traffic signal
def draw_traffic():
    # Draw signal box
    draw_filled_rectangle(400, 200, 450, 400, (0.2, 0.2, 0.2))  # Gray box








    # Draw red light
    draw_filled_circle(425, 370, 15, RED if current_color == RED else (0.5, 0.5, 0.5))  # Dim if not active




    # Draw yellow light
    draw_filled_circle(425, 310, 15, YELLOW if current_color == YELLOW else (0.5, 0.5, 0.5))  # Dim if not active




    # Draw green light
    draw_filled_circle(425, 250, 15, GREEN if current_color == GREEN else (0.5, 0.5, 0.5))  # Dim if not active




def display():
    global is_day, thunder_occurred, bx, lx




    # Set background color based on day or night
    if is_day:
        glClearColor(0.53, 0.81, 0.92, 1.0)  # Sky blue for day
        sun_color = (1.0, 0.85, 0.2)  # Yellow sun for day
    else:
        glClearColor(0.1, 0.1, 0.2, 1.0)  # Dark blue for night
        sun_color = (0.9, 0.9, 0.9)  # Light gray sun (moon) for night




    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)
    draw_river()
    draw_hills()
    draw_fields()


    # Draw clouds continuously
    small_clouds()
    large_clouds()


    # Draw the buildings
    building_color = (0.8, 0.52, 0.25)  # Light brick color
    window_color = (0.9, 0.9, 0.9)  # Light window color
    # Building 1
    draw_building(50, 200, 80, 120, building_color, window_color)  # Left-most building
    # Building 2
    draw_building(200, 200, 90, 130, building_color, window_color)  # Slightly wider
    # Building 3
    draw_building(350, 200, 100, 150, building_color, window_color)  # Taller
    # Building 4
    draw_building(500, 200, 80, 110, building_color, window_color)  # Standard size
    # Building 5
    draw_building(650, 200, 90, 140, building_color, window_color)  # Wider and taller


    # Draw the sun or moon
    draw_circle(650, 500, 50, sun_color)  # Sun or moon at the top right
   
    # Draw stars during night
    if not is_day:
        draw_stars()


    # Handle rain
    if raindrops_falling:
        draw_rain()
        update_raindrops()
        generate_raindrop()
       
        # Generate thunder after every 10 raindrops
        if len(raindrops_list) % 10 == 0:
            thunder_occurred = True
            generate_thunder()
    # Handle snow
    if snowfall_active:
        draw_snow()
        update_snowflakes()
        generate_snowflake()


    # Draw road and its elements
    draw_road()
    draw_traffic_signal()


    # Draw upper road trees and lamps
    for i, tree_obj in enumerate(trees):
        if i % 2 == 0:  # Upper road trees
            tree_obj.draw()
    for lamp_obj in lamps:
        if lamp_obj.y == 145:  # Upper road lamps
            lamp_obj.draw()


    # Draw cars
    for car in cars:
        car.update()
        car.draw()


    # Draw lower road trees and lamps
    for i, tree_obj in enumerate(trees):
        if i % 2 == 1:  # Lower road trees
            tree_obj.draw()
    for lamp_obj in lamps:
        if lamp_obj.y == 55:  # Lower road lamps
            lamp_obj.draw()




    glFlush()  # Ensure the scene is rendered after all updates
    glutPostRedisplay()  # Redraw the scene to update continuously




def keyboard(key, x, y):
    """Handle key press events."""
    global is_day, raindrops_falling, snowfall_active, snowflakes_list, raindrops_list, thunder_occurred,signal_state, car_moving,current_color
   
    if key == b'0':  # Press '0' for yellow
       
        current_color = YELLOW
        glutPostRedisplay()  # Redraw the screen after color change
        time.sleep(1)  # Wait 2 seconds before changing to red
        current_color = RED
        signal_state=False
        glutPostRedisplay() # Redraw after changing to red
    elif key == b'1':  # Press '1' for green
        current_color = GREEN
        signal_state=True
        glutPostRedisplay()  # Redraw the screen after color change
    if key == b'n':  # Switch to night
        is_day = False
        glutPostRedisplay()  # Redraw the scene
    elif key == b'd':  # Switch to day
        is_day = True
        glutPostRedisplay()  # Redraw the scene
    elif key == b'r':  # Start the rain
        if not raindrops_falling:
            raindrops_falling = True
            snowfall_active = False
            for _ in range(150):  # Initialize raindrops when they start falling
                generate_raindrop()
        glutPostRedisplay()
    elif key == b's':  # Stop the rain
        raindrops_falling = False
        raindrops_list.clear()  # Clear the list of raindrops
        thunder_occurred = False
        glutPostRedisplay()
    elif key == b'w':  # Start or stop snowfall
        snowfall_active = not snowfall_active
        raindrops_falling = False
        if snowfall_active:
            for _ in range(150):  # Initialize snowflakes
                generate_snowflake()
        else:
            snowflakes_list.clear()  # Clear snowflakes when snowfall stops
        glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Raindrop Animation with Thunder")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
   
if __name__ == "__main__":
  main()

