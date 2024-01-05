from PIL import Image
import matplotlib.pyplot as plt
import os
import math


def is_color_within_range(actual_color, target_color, tolerance):
    for a, t in zip(actual_color, target_color):
        #print(a)
        #print(t)
        if abs(a - t) > tolerance:
            return False
    return True

def search_for_color(image_path, target_color, tolerance):
    image = Image.open(image_path)
    width, height = image.size

    target_color = tuple(map(int, target_color))
    matched_coordinates=[] #list to store matched coordinates

    for y in range(height):
        for x in range(width):
            pixel_color = image.getpixel((x, y))


            if is_color_within_range(pixel_color, target_color, tolerance):
                print(f"Color found at coordinates: ({x}, {y})")
                matched_coordinates.append((x,y))

    return matched_coordinates

def plot_image_with_markers(image_path, matched_coordinates):
    image = Image.open(image_path)

    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
        print('true')

    # Plot the image
    plt.imshow(image)

    # Plot markers at matched coordinates
    for x, y in matched_coordinates:
        plt.scatter(x, y, color='red', marker='x', s=50)

    plt.title('Image with Markers')
    plt.show()



def process_images_in_directory(directory_path):
    visited_pixels=[]
    unique_values=set()
    my_dict={}
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(directory_path, filename)

            rgba_image=Image.open(image_path)
            image=rgba_image.convert('RGB')
            #image = Image.open(image_path)
            width, height = image.size


            #for y in range(height):
                #for x in range(width):
            pixel_color = image.getpixel((304, 237))
            if pixel_color!=(255,255,255) and pixel_color!=(0,0,0):
                    #print(pixel_color)
                        if pixel_color not in unique_values:
                             unique_values.add(pixel_color)
                             visited_pixels.append(pixel_color)
                             my_dict.update({pixel_color:image_path})


    print(visited_pixels)
    print(len(visited_pixels))


    closest_colour=find_closest_color((255,218,27),visited_pixels)
    print(closest_colour)
    print(my_dict[closest_colour])

                        #for i in visited_pixels:
                            #print(i)
                            #if pixel_color!=i:

            #if matched_coordinates:
                #plot_image_with_markers(image_path, matched_coordinates)




def find_closest_color(input_color, visited_pixels):
    # Calculate Euclidean distance for each RGB coordinate
    distances = [math.sqrt(sum((a - b) ** 2 for a, b in zip(input_color, rgb))) for rgb in visited_pixels]

    # Find the index of the minimum distance
    min_distance_index = distances.index(min(distances))

    # Return the RGB coordinate with the minimum distance
    return visited_pixels[min_distance_index]


# Example usage
image_path = r"C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\images\R403-04-03_ON_20230912T113546_S1-100_A5.6.jpg"  # Change this to your image file path
directory_path=r'C:\Users\Harry.Delalis\PycharmProjects\cell_gap_matching_to_michel_levy\colour_images'
target_color = (0,0,0)  # Replace with your target RGB color
tolerance=10
#matched_coordinates=search_for_color(image_path,target_color,tolerance)
#search_for_color(image_path, target_color, tolerance)
#plot_image_with_markers(image_path,matched_coordinates)

process_images_in_directory(directory_path)


