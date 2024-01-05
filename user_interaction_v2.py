import matplotlib.pyplot as plt
from PIL import Image

def extract_color(image, x, y):
    # Open the image using Pillow (PIL)
    img = Image.open(image)
    # Get the RGB values of the selected pixel
    color = img.getpixel((x, y))

    return color

# Load your image
image_path = r"C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\images\R486-02-ON_collage.jpg"
img = plt.imread(image_path)

# Create a figure and display the image
fig, ax = plt.subplots()
ax.imshow(img)


# Prompt the user to click on points to define a rectangle
points = plt.ginput(input(), timeout=-1)
print(points)

x_coordinates=[]
y_coordinates=[]
for i in range(len(points)):
    x_coordinates.append(points[i][0])
    y_coordinates.append(points[i][1])
    selected_color=extract_color(image_path,x_coordinates[i],y_coordinates[i])
    print(f"Color at ({x_coordinates[i]}, {y_coordinates[i]}): {selected_color}")

# Show the image with the selected region
#plt.imshow(img)
plt.show()



