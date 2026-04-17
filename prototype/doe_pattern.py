import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft2, ifft2

N = 2048                     # high-res for sharp printing
np.random.seed(42)

# Target cross (slightly thicker arms for visible room demo)
target = np.zeros((N, N))
arm_thickness = int(N * 0.08)
center = N // 2
target[center - arm_thickness//2 : center + arm_thickness//2, :] = 1.0
target[:, center - arm_thickness//2 : center + arm_thickness//2] = 1.0
target /= np.sum(target)

# Gerchberg-Saxton algorithm
amplitude_target = np.sqrt(target)
phase = 2 * np.pi * np.random.rand(N, N)
field = amplitude_target * np.exp(1j * phase)

for _ in range(8):          # more iterations = cleaner cross
    input_field = ifft2(field)
    input_phase = np.angle(input_field)
    input_complex = np.exp(1j * input_phase)
    field = fft2(input_complex)
    field = amplitude_target * np.exp(1j * np.angle(field))

doe_phase = np.angle(input_complex) % (2 * np.pi)

# Printable versions
grayscale_doe = (doe_phase / (2 * np.pi) * 255).astype(np.uint8)
binary_doe = np.where(grayscale_doe > 127, 255, 0)

# Save for printing
plt.imsave('doe_grayscale_print.png', grayscale_doe, cmap='gray', dpi=300)
plt.imsave('doe_binary_print.png', binary_doe, cmap='gray', dpi=300)

print("✅ Saved: doe_grayscale_print.png and doe_binary_print.png")
print("Print the grayscale version first — it usually gives the best results.")
