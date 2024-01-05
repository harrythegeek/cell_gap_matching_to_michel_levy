#Testing_3.py
#user_interaction_v2.py

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
import math


def add_text_marker(image_path, coordinates, text,  text_color=(255, 0, 0)):
    # Open the image
    image = Image.open(image_path)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Specify the font and size
    #font = ImageFont.load_default()
    font=ImageFont.truetype(r'open-sans/OpenSans-Bold.ttf', size=70)

    # Extract coordinates
    x, y = coordinates

    # Draw the text marker
    draw.text((x, y), text, font=font, fill=text_color)

    # Save or display the modified image
    #image.show()
    # Alternatively, you can save the modified image
    image.save("output_image.jpg")



def extract_color(image, x, y):
    # Open the image using Pillow (PIL)
    img = Image.open(image)
    # Get the RGB values of the selected pixel
    color = img.getpixel((x, y))

    return color

# Load your image
image_path = r"C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\images\R403-04-03_ON_20230912T113546_S1-100_A5.6.jpg"
image_path_2=r"C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\output_image.jpg"
#directory_path = r'C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\colour_images'

img = plt.imread(image_path)

# Create a figure and display the image
fig, ax = plt.subplots()
ax.imshow(img)




# Prompt the user to click on points to define a rectangle
points = plt.ginput(100, timeout=-1)
print('points selected:',points)

x_coordinates=[]
y_coordinates=[]
colour_database=[]
xy_coordinates=[]

for i in range(len(points)):
    x_coordinates.append(points[i][0])
    y_coordinates.append(points[i][1])
    selected_color=extract_color(image_path,x_coordinates[i],y_coordinates[i])
    print(f"Color at ({x_coordinates[i]}, {y_coordinates[i]}): {selected_color}")

    colour_database.append(selected_color)
    xy_coordinates.append(points)


def is_color_within_range(actual_color, target_color, tolerance):
    for a, t in zip(actual_color, target_color):
        # print(a)
        # print(t)
        if abs(a - t) > tolerance:
            return False
    return True


def search_for_color(image_path, target_color, tolerance):
    image = Image.open(image_path)
    width, height = image.size

    target_color = tuple(map(int, target_color))
    matched_coordinates = []  # list to store matched coordinates

    for y in range(height):
        for x in range(width):
            pixel_color = image.getpixel((x, y))

            if is_color_within_range(pixel_color, target_color, tolerance):
                print(f"Color found at coordinates: ({x}, {y})")
                matched_coordinates.append((x, y))

    return matched_coordinates


def plot_image_with_markers(image_path, matched_coordinates):
    image = Image.open(image_path)

    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Plot the image
    plt.imshow(image)

    # Plot markers at matched coordinates
    for x, y in matched_coordinates:
        plt.scatter(x, y, color='red', marker='x', s=50)

    plt.title('Image with Markers')
    plt.show()


def process_images_in_directory(directory_path):
    visited_pixels = []
    unique_values = set()
    my_dict = {}
    closest_colour_database=[]
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(directory_path, filename)

            rgba_image = Image.open(image_path)
            image = rgba_image.convert('RGB')
            # image = Image.open(image_path)
            width, height = image.size

            # for y in range(height):
            # for x in range(width):
            pixel_color = image.getpixel((304, 237))
            if pixel_color != (255, 255, 255) and pixel_color != (0, 0, 0):
                # print(pixel_color)
                if pixel_color not in unique_values:
                    unique_values.add(pixel_color)
                    visited_pixels.append(pixel_color)
                    my_dict.update({pixel_color: image_path})


    for z in colour_database:
        print('colour picked',z)
        closest_colour = find_closest_color(z, visited_pixels)
        print('closest colour',closest_colour)
        print('image associated with the closest colour',my_dict[closest_colour])
        closest_colour_database.append(closest_colour)

    return my_dict,closest_colour_database

    # for i in visited_pixels:
    # print(i)
    # if pixel_color!=i:

    # if matched_coordinates:
    # plot_image_with_markers(image_path, matched_coordinates)


def find_closest_color(input_color, visited_pixels):
    # Calculate Euclidean distance for each RGB coordinate
    distances = [math.sqrt(sum((a - b) ** 2 for a, b in zip(input_color, rgb))) for rgb in visited_pixels]

    # Find the index of the minimum distance
    min_distance_index = distances.index(min(distances))

    # Return the RGB coordinate with the minimum distance
    return visited_pixels[min_distance_index]

# Example usage
#image_path = r"C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\images\R486-02-ON_collage.jpg"  # Change this to your image file path
directory_path = r'C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\colour_images'
target_color = (0, 0, 0)  # Replace with your target RGB color
tolerance = 10
#matched_coordinates=search_for_color(image_path,target_color,tolerance)
#search_for_color(image_path, target_color, tolerance)
#plot_image_with_markers(image_path,matched_coordinates)



dictionary,closest_colour_database=process_images_in_directory(directory_path)





    #for the first iteration it will take the original image path
    #for the second iteration it will take the image created with the writing on it

for i in range(len(colour_database)):
    print(i)
    print(colour_database[i])

for q in range(len(closest_colour_database)):
    original_string=dictionary[closest_colour_database[q]]
    start_index=93
    end_index=97
    desired_part=original_string[start_index:end_index]
    print('original string',original_string)

    #for i in range(len(points)):
    if q==0:
            add_text_marker(image_path, points[q], text=desired_part)
    else:
            add_text_marker(image_path_2,points[q], text=desired_part)


# Show the image with the selected region
#plt.imshow(img)
plt.show()




#print('this is the dictionary printed outside of the def',dictionary)

