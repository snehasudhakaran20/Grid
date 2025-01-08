import numpy as np

def amaze_demosaic(bayer_image):
    """
    Full AMaZE-like demosaicing for an NxN Bayer-patterned grid.

    Parameters:
        bayer_image (np.ndarray): Input Bayer-patterned image (NxN array).

    Returns:
        rgb_image (np.ndarray): Output demosaiced image (NxNx3 array).
    """
    # Get dimensions
    height, width = bayer_image.shape

    # Initialize the RGB image
    rgb_image = np.zeros((height, width, 3), dtype=np.float32)

    # Helper function for directional gradients
    def calculate_gradients(image, x, y):
        g_h = abs(image[x, y - 1] - image[x, y + 1])
        g_v = abs(image[x - 1, y] - image[x + 1, y])
        return g_h, g_v

    # Green Channel Interpolation
    green_channel = np.zeros_like(bayer_image)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                # Pixel is green
                green_channel[i, j] = bayer_image[i, j]
            else:
                # Interpolate green
                g_h, g_v = calculate_gradients(bayer_image, i, j)
                if g_h < g_v:
                    green_channel[i, j] = (bayer_image[i, j - 1] + bayer_image[i, j + 1]) / 2
                elif g_v < g_h:
                    green_channel[i, j] = (bayer_image[i - 1, j] + bayer_image[i + 1, j]) / 2
                else:
                    green_channel[i, j] = (bayer_image[i, j - 1] + bayer_image[i, j + 1] +
                                           bayer_image[i - 1, j] + bayer_image[i + 1, j]) / 4

    rgb_image[:, :, 1] = green_channel  # Assign green channel

    # Red and Blue Channel Interpolation
    red_channel = np.zeros_like(bayer_image)
    blue_channel = np.zeros_like(bayer_image)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if i % 2 == 0 and j % 2 == 0:
                # Pixel is red
                red_channel[i, j] = bayer_image[i, j]
                # Interpolate blue
                blue_channel[i, j] = (bayer_image[i - 1, j - 1] + bayer_image[i - 1, j + 1] +
                                      bayer_image[i + 1, j - 1] + bayer_image[i + 1, j + 1]) / 4
            elif i % 2 == 1 and j % 2 == 1:
                # Pixel is blue
                blue_channel[i, j] = bayer_image[i, j]
                # Interpolate red
                red_channel[i, j] = (bayer_image[i - 1, j - 1] + bayer_image[i - 1, j + 1] +
                                     bayer_image[i + 1, j - 1] + bayer_image[i + 1, j + 1]) / 4
            else:
                # Interpolate red and blue for green pixels
                g_h, g_v = calculate_gradients(bayer_image, i, j)
                if g_h < g_v:
                    red_channel[i, j] = (bayer_image[i, j - 1] + bayer_image[i, j + 1]) / 2
                    blue_channel[i, j] = (bayer_image[i - 1, j] + bayer_image[i + 1, j]) / 2
                else:
                    red_channel[i, j] = (bayer_image[i - 1, j] + bayer_image[i + 1, j]) / 2
                    blue_channel[i, j] = (bayer_image[i, j - 1] + bayer_image[i, j + 1]) / 2

    rgb_image[:, :, 0] = red_channel  # Assign red channel
    rgb_image[:, :, 2] = blue_channel  # Assign blue channel

    # Refinement Step
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if (i + j) % 2 == 0:
                # Residual correction for aliasing
                r_residual = (green_channel[i, j] - (red_channel[i, j - 1] + red_channel[i, j + 1]) / 2)
                b_residual = (green_channel[i, j] - (blue_channel[i - 1, j] + blue_channel[i + 1, j]) / 2)
                red_channel[i, j] += r_residual
                blue_channel[i, j] += b_residual

    return rgb_image

# Example Usage
# Create a sample NxN Bayer pattern image (example: 6x6 grid)
bayer_image = np.array([
    [255, 0, 255, 0, 255, 0],
    [0, 128, 0, 128, 0, 128],
    [255, 0, 255, 0, 255, 0],
    [0, 128, 0, 128, 0, 128],
    [255, 0, 255, 0, 255, 0],
    [0, 128, 0, 128, 0, 128]
], dtype=np.float32)

# Demosaic the image
rgb_image = amaze_demosaic(bayer_image)

print("Demosaiced RGB Image:")
print(rgb_image)
