# Stellar Dominion

[![Pylint](https://github.com/lispmeister/lunar-cross/actions/workflows/pylint.yml/badge.svg)](https://github.com/lispmeister/lunar-cross/actions/workflows/pylint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10-blue)](prototype/lunar-cross-visualization.py)

![Stellar Dominion Promo](docs/images/lunar-cross-promo.jpeg?v=2)

> *For we are God's handiwork, created in Christ Jesus to do good works,
> which God prepared in advance for us to do.*
> — Ephesians 2:10 (NIV)

## What Is This?

A kilowatt-class emerald-green laser, mounted in a permanently-landed SpaceX
Starship on the Moon's north pole, projecting a cross-shaped beam visible to
the naked eye across all 48 contiguous United States — every Sunday night, for
as long as we choose to keep it on.

Not science fiction. Every component exists today.

## Key Facts

| Parameter | Value |
|---|---|
| Platform | SpaceX Starship HLS (permanent lunar installation) |
| Location | Lunar north pole, peak of eternal light |
| Wavelength | 532 nm emerald green |
| Optical power | 3–5 kW |
| Cross angular span | 0.7° (covers the continental US) |
| System mass | ~1.4 tonnes |
| Core project cost | $42–114M (launch separate) |
| Operation | Sundays only; first light target Easter 2027 |

## Documentation

- **[Design & Calculations (Markdown)](docs/DESIGN-AND-CALCULATIONS.md)** —
  engineering reference: all calculations, mass budget, power system, cost
  estimates, and timeline
- **[Design & Calculations (PDF/LaTeX)](docs/design-and-calculations.tex)** —
  full pitch document with figures; compile with `pdflatex`

## Prototype

The `prototype/` directory contains two Python scripts:

- **`lunar-cross-visualization.py`** — scientifically accurate sky diagram
  showing the cross at true angular scale as seen from the US
- **`doe_pattern.py`** — Gerchberg–Saxton algorithm generating a printable
  diffractive optical element (DOE) phase mask for tabletop demos

Requires [uv](https://github.com/astral-sh/uv).

```bash
cd prototype
uv venv
uv pip install -r requirements.txt
uv run lunar-cross-visualization.py   # sky diagram
uv run doe_pattern.py                 # DOE phase mask
```

## Why?

Because some things deserve to exist simply for the awe they inspire.

Stellar Dominion would be the first human-made structure visible from Earth
with the naked eye beyond low orbit — proof that we are a species capable of
leaving a mark of beauty on another world. Every child who looks up and sees it
will know: *we built that.*

The engineering is feasible. The physics is settled. The question is no longer
*can we* — it is *will we*.
