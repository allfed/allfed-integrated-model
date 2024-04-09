""" 
In your command line, be sure to run the following if you update the Dot images:

dot -Tpng overview.dot -o overview.png
dot -Tpng overview_legend.dot -o overview_legend.png

Then to form the complete diagram, run the python script below:

"""

from PIL import Image

# Load the images
image1_path = "overview.png"
image2_path = "overview_legend.png"
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

# Calculate the size of the combined image
total_width = max(image1.width, image2.width)
total_height = image1.height + image2.height

# Create a new image with the appropriate size and white background
combined_image = Image.new(
    "RGB", (int(total_width * 1.1), total_height - image2.height // 2), color="white"
)

# Paste the first image at the top
combined_image.paste(image1, (int(total_width * 0.1), 0))

# Paste the second image at the bottom
combined_image.paste(image2, (0, image1.height - image2.height // 2))

# Save the combined image
combined_image_path = "../overview.png"
combined_image.save(combined_image_path)
