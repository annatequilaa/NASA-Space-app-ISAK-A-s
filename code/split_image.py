from PIL import Image

def get_hue_saturation_brightness(chunk):
    # Convert the image chunk to HSV (Hue, Saturation, Value)
    hsv_image = chunk.convert("HSV")

    # Get pixel data and calculate average values for hue, saturation, and brightness (value)
    pixels = list(hsv_image.getdata())

    # Separate into individual channels
    hue_values = [pixel[0] for pixel in pixels]        # Hue channel
    saturation_values = [pixel[1] for pixel in pixels] # Saturation channel
    brightness_values = [pixel[2] for pixel in pixels] # Brightness (value) channel

    # Calculate the average hue, saturation, and brightness
    avg_hue = sum(hue_values) / len(hue_values)
    avg_saturation = sum(saturation_values) / len(saturation_values)
    avg_brightness = sum(brightness_values) / len(brightness_values)

    return avg_hue, avg_saturation, avg_brightness

def split_image(size):
    image = Image.open("space.jpg")

    chunk_width = size
    chunk_height = size

    img_width, img_height = image.size 
    chunks = []
    chunk_attributes = []  # List to store attributes

    for top in range(0, img_height, chunk_height):
        for left in range(0, img_width, chunk_width):
            # Define the box (left, upper, right, lower)
            box = (left, top, left + chunk_width, top + chunk_height)
            
            # Crop the image using the box
            chunk = image.crop(box)
            
            # Save each chunk as a separate image file or append to a list
            chunks.append(chunk)
            
            # Get the hue, saturation, and brightness for the chunk
            avg_hue, avg_saturation, avg_brightness = get_hue_saturation_brightness(chunk)
            
            # Get and store attributes like dimensions and color mode
            chunk_size = chunk.size  # (width, height)
            chunk_mode = chunk.mode  # Color mode (e.g., 'RGB')

            # Append the attributes directly as a list
            chunk_attributes.append([
                int(avg_hue),            # average hue
                int(avg_saturation),     # average saturation
                int(avg_brightness)      # average brightness
            ])
    
    return chunk_attributes

attributes = split_image(100)
print(attributes)


