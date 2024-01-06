import cv2
import numpy as np

# Global variables for storing selected points
selected_points = []

# Mouse callback function for selecting points
def select_point(event, x, y, flags, param):
    global selected_points

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Select Points', img)

# Read the image with the color chart
img_path = r'C:\Users\User\PycharmProjects\cell_gap_matching_to_michel_levy\images\R403-02(2).jpg'  # Replace with the path to your calibration image
img = cv2.imread(img_path)

# Check if the image is successfully loaded
if img is None:
    print(f"Error: Unable to load the image from {img_path}")
else:
    # Create a window for selecting points
    cv2.namedWindow('Select Points')
    cv2.setMouseCallback('Select Points', select_point)

    # Display the image and wait for user to select points
    cv2.imshow('Select Points', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Extract color values from the selected points
    extracted_colors = np.array([img[y, x] for x, y in selected_points])

    # Define the known color values of the color chart
    color_chart_values = np.array([[255, 0, 0],  # Red
                                   [0, 255, 0],  # Green
                                   [0, 0, 255],  # Blue
                                   [255, 255, 0],  # Yellow
                                   [0, 255, 255],  # Cyan
                                   [255, 0, 255]])  # Magenta

    print(len(color_chart_values))
    print(len(selected_points))

    # Check if the number of selected points matches the size of color_chart_values
    if len(selected_points) == len(color_chart_values):
        print(len(selected_points))
        # Calculate the color correction matrix
        color_correction_matrix = np.linalg.inv(
            np.vstack((extracted_colors.T, np.ones((1, len(selected_points)))))).dot(
            np.vstack((color_chart_values.T, np.ones((1, len(selected_points))))))

        # Apply color correction to the entire image
        img_corrected = cv2.transform(img, color_correction_matrix.T[:3, :])

        # Display the original and corrected images
        cv2.imshow('Original Image', img)
        cv2.imshow('Corrected Image', img_corrected)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Number of selected points does not match the size of color_chart_values.")
