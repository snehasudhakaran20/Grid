import numpy as np

def gaussian_kernel(size, sigma):
    """
    Generate a Gaussian kernel.

    Args:
        size (int): The size of the kernel (e.g., 3 for a 3x3 kernel).
        sigma (float): The standard deviation of the Gaussian.

    Returns:
        np.ndarray: A 2D Gaussian kernel.
    """
    kernel = np.zeros((size, size), dtype=float)
    offset = size // 2
    for i in range(size):
        for j in range(size):
            x = i - offset
            y = j - offset
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)  # Normalize
    return kernel

def apply_gaussian_blur(grid, kernel):
    """
    Apply Gaussian blur to a grid of pixels.

    Args:
        grid (np.ndarray): 2D array representing the pixel grid.
        kernel (np.ndarray): 2D Gaussian kernel.

    Returns:
        np.ndarray: Blurred grid.
    """
    grid = np.pad(grid, pad_width=kernel.shape[0] // 2, mode='constant', constant_values=0)  # Padding
    blurred_grid = np.zeros_like(grid)

    kernel_size = kernel.shape[0]
    offset = kernel_size // 2

    for i in range(offset, grid.shape[0] - offset):
        for j in range(offset, grid.shape[1] - offset):
            region = grid[i - offset:i + offset + 1, j - offset:j + offset + 1]
            blurred_grid[i, j] = np.sum(region * kernel)

    return blurred_grid[offset:-offset, offset:-offset]  # Remove padding


if __name__ == "__main__":
    main()
