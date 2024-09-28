from PIL import Image

# Load the images
image1_path = "overview.png"
image2_path = "overview_legend.png"
image1 = Image.open(image1_path).convert(
    "RGBA"
)  # Ensure image1 supports transparency
image2 = Image.open(image2_path).convert(
    "RGBA"
)  # Ensure image2 supports transparency

# Make white in image2 transparent
datas = image2.getdata()
new_data = []
for item in datas:
    # Change all white (also shades of white)
    if item[:3] == (255, 255, 255):  # Detect white
        new_data.append((255, 255, 255, 0))  # Make it transparent
    else:
        new_data.append(item)
image2.putdata(new_data)

# Calculate the size of the combined image
total_width = max(image1.width, image2.width)
total_height = image1.height + image2.height

shift_right_fraction = 0
start_y_position_of_second_image = total_height - image2.height * 1.35

# Create a new image with transparency support (RGBA mode)
combined_image = Image.new(
    "RGB",  # Use RGBA for transparency
    (
        int(total_width * (1 + shift_right_fraction)),
        int(start_y_position_of_second_image + image2.height),
    ),
    (255, 255, 255, 0),  # Fully transparent background
)

# Paste the first image at the top
combined_image.paste(
    image1, (int(total_width * shift_right_fraction), 0), image1
)

# Paste the second image (with transparency) below
combined_image.paste(image2, (0, int(start_y_position_of_second_image)), image2)

# Save the combined image
combined_image_path = "../overview.png"
combined_image.save(combined_image_path)
