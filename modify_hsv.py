import cv2
import numpy as np

# Read the image
img_path = r'C:\Users\User\PycharmProjects\cell_gap_matching_to_michel_levy\images\R403-02(2).jpg'  # Replace with the path to your image
img = cv2.imread(img_path)

# Check if the image is successfully loaded
if img is None:
    print(f"Error: Unable to load the image from {img_path}")
else:
    # Convert the image to HSV color space
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # User input for target brightness and saturation values (between 0 and 1)
    target_brightness = float(input("Enter target brightness (0 to 1): "))
    target_saturation = float(input("Enter target saturation (0 to 1): "))

    # Calculate the current mean brightness and saturation
    mean_brightness = cv2.mean(img_hsv)[2] / 255.0
    mean_saturation = cv2.mean(img_hsv)[1] / 255.0

    # Calculate the scaling factors for brightness and saturation
    brightness_scale = target_brightness / mean_brightness
    saturation_scale = target_saturation / mean_saturation

    # Adjust brightness and saturation
    img_hsv[:, :, 2] = np.clip(cv2.multiply(img_hsv[:, :, 2], brightness_scale), 0, 255)
    img_hsv[:, :, 1] = np.clip(cv2.multiply(img_hsv[:, :, 1], saturation_scale), 0, 255)

    # Convert back to BGR color space
    modified_img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    # Display the original and modified images
    cv2.imshow('Original Image', img)
    cv2.imshow('Modified Image', modified_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the modified image
    output_path = r'C:\Users\User\PycharmProjects\cell_gap_matching_to_michel_levy\images\edited_image.jpg'  # Replace with the desired output path
    cv2.imwrite(output_path, modified_img)
    print(f"Modified image saved to {output_path}")
