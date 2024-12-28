import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.datasets import load_sample_image

# Load an example image
test = load_sample_image("test.jpg")
gray_image = np.mean(test, axis=2)  # Convert to grayscale
gray_image = gray_image[:64, :64]  # Resize for simplicity

plt.imshow(gray_image, cmap='gray')
plt.title("Original Image")
plt.show()

# Flatten the image
pixels = gray_image.flatten().reshape(-1, 1)

# Apply PCA
pca = PCA(n_components=10)  # Retain top 10 principal components
compressed = pca.fit_transform(pixels)

# Reconstruct the image
reconstructed = pca.inverse_transform(compressed).reshape(gray_image.shape)

# Show the reconstructed image
plt.imshow(reconstructed, cmap='gray')
plt.title("Reconstructed Image with 10 Components")
plt.show()
