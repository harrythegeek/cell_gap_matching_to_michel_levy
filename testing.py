from PIL import Image

def convert_png_to_jpg(png_path, jpg_path):
    # Open the PNG image
    png_img = Image.open(png_path)

    # Convert and save as JPG
    png_img.convert("RGB").save(jpg_path, "JPEG")

def match_brightness(reference_path, input_path, output_path):
    # Open the reference and input images
    reference_img = Image.open(reference_path)
    input_img = Image.open(input_path)

    # Convert images to grayscale
    reference_img_gray = reference_img.convert("L")
    input_img_gray = input_img.convert("L")

    # Get the brightness of the reference image
    reference_brightness = reference_img_gray.histogram().index(max(reference_img_gray.histogram()))

    # Get the brightness of the input image
    input_brightness = input_img_gray.histogram().index(max(input_img_gray.histogram()))

    # Calculate the adjustment factor
    adjustment_factor = reference_brightness / input_brightness

    # Adjust the brightness of the input image
    adjusted_img = input_img.point(lambda x: x * adjustment_factor)

    # Save the adjusted image
    adjusted_img.save(output_path)


if __name__ == "__main__":

    png_image_path = "reference.png"
    jpg_image_path = "reference_converted.jpg"

    convert_png_to_jpg(png_image_path, jpg_image_path)

    reference_image_path = "reference_converted.jpg"
    input_image_path = "sample_1.jpg"
    output_image_path = "adjusted_5.jpg"


    match_brightness(reference_image_path, input_image_path, output_image_path)
