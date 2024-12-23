import numpy as np

def interpolate_green_channel(bayer_grid):
    """
    Interpolate the green channel from the Bayer pattern.

    Args:
        bayer_grid (np.ndarray): 2D Bayer pattern grid.

    Returns:
        np.ndarray: Interpolated green channel.
    """
    height, width = bayer_grid.shape
    green_channel = np.zeros_like(bayer_grid, dtype=float)

    # Assume RGGB pattern
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                # Green pixels directly
                green_channel[i, j] = bayer_grid[i, j]
            else:
                # Interpolation for non-green pixels
                green_channel[i, j] = 0.25 * (
                    bayer_grid[i - 1, j] +
                    bayer_grid[i + 1, j] +
                    bayer_grid[i, j - 1] +
                    bayer_grid[i, j + 1]
                )
    return green_channel

def interpolate_red_and_blue_channels(bayer_grid, green_channel):
    """
    Interpolate the red and blue channels from the Bayer pattern.

    Args:
        bayer_grid (np.ndarray): 2D Bayer pattern grid.
        green_channel (np.ndarray): Interpolated green channel.

    Returns:
        tuple: Interpolated red and blue channels.
    """
    height, width = bayer_grid.shape
    red_channel = np.zeros_like(bayer_grid, dtype=float)
    blue_channel = np.zeros_like(bayer_grid, dtype=float)

    # Assume RGGB pattern
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if i % 2 == 0 and j % 2 == 0:
                # Red pixel
                red_channel[i, j] = bayer_grid[i, j]
                blue_channel[i, j] = 0.25 * (
                    bayer_grid[i - 1, j - 1] +
                    bayer_grid[i - 1, j + 1] +
                    bayer_grid[i + 1, j - 1] +
                    bayer_grid[i + 1, j + 1]
                )
            elif i % 2 == 1 and j % 2 == 1:
                # Blue pixel
                blue_channel[i, j] = bayer_grid[i, j]
                red_channel[i, j] = 0.25 * (
                    bayer_grid[i - 1, j - 1] +
                    bayer_grid[i - 1, j + 1] +
                    bayer_grid[i + 1, j - 1] +
                    bayer_grid[i + 1, j + 1]
                )
            else:
                # Non-red and non-blue pixels
                red_channel[i, j] = 0.25 * (
                    bayer_grid[i, j - 1] +
                    bayer_grid[i, j + 1] +
                    bayer_grid[i - 1, j] +
                    bayer_grid[i + 1, j]
                )
                blue_channel[i, j] = 0.25 * (
                    bayer_grid[i, j - 1] +
                    bayer_grid[i, j + 1] +
                    bayer_grid[i - 1, j] +
                    bayer_grid[i + 1, j]
                )
    return red_channel, blue_channel

def amaze_demosaic(bayer_grid):
    """
    Perform AMAZE-like demosaicing on a Bayer grid.

    Args:
        bayer_grid (np.ndarray): 2D Bayer pattern grid.

    Returns:
        np.ndarray: RGB image.
    """
    green_channel = interpolate_green_channel(bayer_grid)
    red_channel, blue_channel = interpolate_red_and_blue_channels(bayer_grid, green_channel)

    rgb_image = np.stack((red_channel, green_channel, blue_channel), axis=-1)
    return rgb_image


