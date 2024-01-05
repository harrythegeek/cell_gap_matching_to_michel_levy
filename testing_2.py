import cv2
import numpy as np

def find_and_mark_pixel(image_path, target_color, marker_color=(0, 255, 0)):
    # Read the image
    image = cv2.imread(image_path)

    # Convert target_color to a numpy array for easier comparison
    target_color = np.array(target_color)
    print(target_color)

    # Find coordinates where the pixel matches the target_color
    matching_coordinates = np.column_stack(np.where(np.all(image == target_color, axis=-1)))
    print(matching_coordinates)

    # Mark the matching coordinates with a point
    for coord in matching_coordinates:
        cv2.circle(image, tuple(coord[::-1]), 5, marker_color, -1)

    # Display the image with marked points
    cv2.imshow('Marked Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Input RGB coordinate (example: red color)
    target_color = [255,255,255]

    # Image path (replace with the path to your image)
    image_path = ''

    # Call the function to find and mark the pixel in the image
    find_and_mark_pixel(image_path, target_color)
