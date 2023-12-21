import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

def on_click(event):
    global x1, y1  # Declare x1 and y1 as global variables

    if event.dblclick:
        # Get the coordinates of the selected region
        x1, y1, x2, y2 = int(event.xdata), int(event.ydata), int(event.xdata), int(event.ydata)
        rect.set_xy((x1, y1))
        rect.set_width(0)
        rect.set_height(0)
        plt.draw()
    elif event.button == 1:
        # Update the coordinates of the selected region
        x2, y2 = int(event.xdata), int(event.ydata)
        rect.set_width(x2 - x1)
        rect.set_height(y2 - y1)
        plt.draw()



def extract_color(image, x, y):
    # Open the image using Pillow (PIL)
    img = Image.open(image)
    # Get the RGB values of the selected pixel
    color = img.getpixel((x, y))
    return color

# Load your image
image_path = 'test_image.jpg'
img = plt.imread(image_path)

# Create a figure and display the image
fig, ax = plt.subplots()
ax.imshow(img)

# Create a Rectangle patch (initially invisible)
rect = Rectangle((0, 0), 0, 0, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

# Connect the event handler function to the 'button_press_event' event
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()

# Wait for the user to close the plot
plt.close()

# Extract and print the color of the selected region
selected_x, selected_y = int(rect.get_x()), int(rect.get_y())
selected_color = extract_color(image_path, selected_x, selected_y)
print(f"Color at ({selected_x}, {selected_y}): {selected_color}")
