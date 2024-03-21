import turtle

class labels_x_axis:
    #a class to write text at specified angle
    def write_tilted_text(self, text_to_write, text_font=("Arial", 11, "normal"), text_alignment="left", angle=0):
        self.screen.write(self._position, str(text_to_write), text_alignment.lower(), text_font, self._pencolor, angle)
        
    def tilted_text(self, position, text, alignment, text_font, text_colour, text_angle):
        x, y = position
        x *= self.xscale  #adjust the x position based on scale factor
        y *= self.yscale  #adjust the y position based on scale factor
        text_rotating_point = {"left":"sw", "center":"s", "right":"se" }  #map the alignment to the appropriate anchor
        item = self.cv.create_text(x-1, -y, text = text, anchor = text_rotating_point[alignment], fill = text_colour, font = text_font, angle = text_angle)


# monkey patching the write method to include rotated text subrouitne

turtle.RawTurtle.write = Rotated_text.write_tilted_text
turtle.TurtleScreenBase.write = Rotated_text.tilted_text


# ===========================================
tt = turtle.Turtle()
text_to_write = 'abc'
tt.speed('normal')
tt.color("green")
sc = turtle.Screen() ; sc.bgcolor("white")
txt_angle1 = 270
tt.setheading(txt_angle1); tt.forward(100)
tt.write(text_to_write, text_font=("Arial", 10, "bold"), text_alignment="right", angle=txt_angle1)
tt.backward(100)

from time import sleep
sleep(100)













# # Function to write text vertically
# def write_vertical(turtle, text, x, y):
#     turtle.penup()
#     turtle.goto(x, y)
#     turtle.pendown()
#     turtle.setheading(90)  # Set turtle to point upwards
#     for char in text:
#         turtle.write(char, align='center', font=('Arial', 12, 'normal'))
#         turtle.forward(15)  # Adjust this value as needed
#         turtle.right(90)  # Rotate turtle to write the next character vertically

# # Create a turtle object
# my_turtle = turtle.Turtle()

# # Write the text vertically at position (x, y)
# write_vertical(my_turtle, "Your text here", 0, 0)

# # Keep the window open until it's manually closed
# turtle.done()
