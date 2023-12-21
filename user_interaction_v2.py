import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

def extract_color(image, x, y):
    # Open the image using Pillow (PIL)
    img = Image.open(image)
    # Get the RGB values of the selected pixel
    color = img.getpixel((x, y))
    return color

# Load your image
image_path = 'michel_levy_for_colour_extraction.jpeg'
img = plt.imread(image_path)

# Create a figure and display the image
fig, ax = plt.subplots()
ax.imshow(img)

# Prompt the user to click on two points to define a rectangle
points = plt.ginput(2, timeout=-1)

# Close the plot after the user has selected the points
#plt.close()

# Extract the coordinates of the selected region
x1, y1 = points[0]
x2, y2 = points[1]

# Draw a rectangle on the selected region
rect = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

# Show the image with the selected region
plt.imshow(img)
plt.show()

# Extract and print the color of the selected region
selected_x, selected_y = int(x1), int(y1)
selected_color = extract_color(image_path, selected_x, selected_y)
print(f"Color at ({selected_x}, {selected_y}): {selected_color}")
