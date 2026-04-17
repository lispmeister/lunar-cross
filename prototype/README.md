# Stellar Dominion — Prototype Scripts

Two Python scripts: one generates a scientifically accurate sky visualization,
the other computes the diffractive optical element (DOE) phase mask used to
shape the laser beam into a cross pattern.

## Prerequisites

- Python 3.8 or later
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip

## Installation

All commands run from the `prototype/` directory.

```bash
cd prototype

# With uv (recommended)
uv venv
uv pip install -r requirements.txt

# With pip
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Dependencies: `numpy`, `matplotlib`, `scipy`

---

## Sky Visualization

**Script:** `lunar-cross-visualization.py`

Generates a calibrated angular sky diagram showing the emerald-green cross as
it would appear to a US observer. All sizes are rendered at exact naked-eye
angular proportions: the Moon at 0.5°, the cross at 0.7° total span with
0.05° arm thickness.

```bash
uv run lunar-cross-visualization.py
```

**Output:**
- `lunar_cross_scientific_visualization_proper_cross.png` — 300 dpi PNG saved
  to the `prototype/` directory
- An interactive plot window opens for inspection

---

## DOE Pattern Generator

**Script:** `doe_pattern.py`

Computes the phase mask for a diffractive optical element (DOE) that reshapes
a Gaussian laser beam into a cross in the far field. Uses the
[Gerchberg–Saxton](https://doi.org/10.1111/j.1365-2818.1972.tb01282.x)
iterative Fourier algorithm: alternates between the target amplitude in the
focal plane and unit-amplitude constraint at the DOE plane until convergence.

```bash
uv run doe_pattern.py
```

**Output:**
- `doe_grayscale_print.png` — 2048×2048 px, 300 dpi grayscale phase mask
- `doe_binary_print.png` — binarized version (higher contrast, more noise)

Both files are written to the working directory.

### Tabletop Demo

Print `doe_grayscale_print.png` onto clear overhead-projector transparency
film using a laser printer (not inkjet — toner gives sharper dots). Shine any
≥1 mW red or green laser pointer through the printed film at a wall 2–5 m
away: the diffracted beam forms a cross pattern, demonstrating the same
far-field beam-shaping principle used by the flight DOE.

**Tips:**
- Print at actual size, highest quality, black & white
- Hold or tape the film flat and perpendicular to the beam, 1–3 cm from the
  aperture
- If the cross is faint, try the binary version or reduce room ambient light
- ~5–20% of light goes into the cross; the bright central spot is the
  undiffracted zero order — normal and expected

**Safety:** Never look directly into the laser beam or its specular reflection.
Class 2/3R pointers are eye-safe for accidental exposure but not for deliberate
staring.
