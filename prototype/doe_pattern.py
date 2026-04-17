"""Generate a Diffractive Optical Element (DOE) phase pattern for a cross target."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft2, ifft2


def main():
    """Run Gerchberg-Saxton to compute a DOE phase pattern and save print-ready images."""
    size = 2048  # high-res for sharp printing
    np.random.seed(42)

    target = np.zeros((size, size))
    arm_thickness = int(size * 0.08)
    center = size // 2
    target[center - arm_thickness//2: center + arm_thickness//2, :] = 1.0
    target[:, center - arm_thickness//2: center + arm_thickness//2] = 1.0
    target /= np.sum(target)

    amplitude_target = np.sqrt(target)
    phase = 2 * np.pi * np.random.rand(size, size)
    field = amplitude_target * np.exp(1j * phase)

    input_complex = np.exp(1j * phase)  # initialised; overwritten each iteration
    for _ in range(8):  # more iterations = cleaner cross
        input_field = ifft2(field)
        input_phase = np.angle(input_field)
        input_complex = np.exp(1j * input_phase)
        field = fft2(input_complex)
        field = amplitude_target * np.exp(1j * np.angle(field))

    doe_phase = np.angle(input_complex) % (2 * np.pi)

    grayscale_doe = (doe_phase / (2 * np.pi) * 255).astype(np.uint8)
    binary_doe = np.where(grayscale_doe > 127, 255, 0)

    plt.imsave('doe_grayscale_print.png', grayscale_doe, cmap='gray', dpi=300)
    plt.imsave('doe_binary_print.png', binary_doe, cmap='gray', dpi=300)

    print("Saved: doe_grayscale_print.png and doe_binary_print.png")
    print("Print the grayscale version first — it usually gives the best results.")


if __name__ == "__main__":
    main()
