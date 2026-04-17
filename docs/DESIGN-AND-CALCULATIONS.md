# Stellar Dominion: Design & Calculations Reference

> For we are God's handiwork, created in Christ Jesus to do good works,
> which God prepared in advance for us to do.
> — *Ephesians 2:10 (NIV)*

This document is the engineering reference for the Stellar Dominion project. It consolidates all design decisions, calculations, and parametric data. The companion LaTeX document (`design-and-calculations.tex`) renders this material into the full pitch document.

---

## 1. Mission Overview

Stellar Dominion integrates a kilowatt-class emerald-green laser projector directly into a SpaceX Starship HLS that lands permanently on the lunar north pole. The Starship becomes the operational base: its 50 m stainless steel hull provides structure, thermal mass, mounting area for SolAero solar panels and radiators, and elevated line-of-sight. A deployable boom extends the laser, telescope, and DOE from the top of the vehicle, pointing roughly horizontally toward Earth. The cross fires every Sunday when the Moon is visible at night over the US, projecting a 0.7° cross simultaneously visible across all 48 contiguous United States. The build targets a 10-month compressed schedule with aspirational first light on Easter Sunday, April 1, 2027 — contingent on Starship availability.

---

## 2. System Architecture

The Stellar Dominion hardware integrates directly into a SpaceX Starship HLS that lands permanently on the lunar north pole. The Starship is not just the delivery vehicle — it is the operational platform. No separate structure is required. All subsystems are passive or autonomously controlled; no human presence is required after commissioning.

**What Starship provides for free:**
- Structure: 50 m stainless steel tower, exceptional rigidity and thermal mass
- Height: laser at ~50 m elevation gives 13 km line-of-sight to horizon, reducing terrain obstruction risk
- Mounting surface: large hull exterior for solar panels and radiators
- Power bus: Starship HLS power infrastructure available for sharing
- Communications: Starship S-band/Ku-band supplemented by minimal custom avionics
- Durability: stainless steel in vacuum — no corrosion, no weather, indefinite structural life

**Stellar Dominion subsystems integrated into Starship:**
- Multi-kW continuous-wave (CW) fiber laser (3–5 kW optical at 532 nm green)
- Meter-scale beam-expanding telescope
- Diffractive optical element (DOE) for cross-pattern beam shaping
- Deployable boom (3–5 m carbon composite + 2-axis gimbal), extending from top of Starship
- SolAero IMM-α solar array (45 m², hull-mounted rollout panels)
- Amprius silicon-anode lithium-ion battery bank (eclipse bridging)
- Hull-mounted radiator panels (~20 m²)
- Pointing/tracking assembly (star tracker + gimbal on boom)
- Minimal custom avionics (shares Starship comms)

---

## 3. Optical Design

### 3.1 Laser

| Parameter | Value |
|---|---|
| Wavelength | 532 nm (frequency-doubled Nd:YAG) or 520–530 nm fiber |
| Optical output power | 3–5 kW |
| Wall-plug efficiency | 30–40% |
| Electrical power draw | 8–15 kW |
| Beam quality | M² < 1.2 (single-mode or near-diffraction-limited) |
| Vendor class | IPG Photonics YLS series, nLIGHT, or equivalent |
| Mass (commercial) | ~150–250 kg |

Green (532 nm) sits at the peak of human photopic response, maximizing perceived brightness per watt. Frequency-doubled Nd:YAG fiber lasers at this power level are commercially available.

### 3.2 Beam Expander (Telescope)

Before reaching the DOE, the raw laser beam must be expanded to meter scale to control diffraction at the Earth–Moon distance.

**Required aperture calculation:**

The far-field half-angle divergence for a Gaussian beam:

```
θ_div = λ / (π × w₀)
```

To keep the cross arm width at 0.05° (= 8.7 × 10⁻⁴ rad) at d = 3.844 × 10⁸ m:

```
Required spot radius at Earth:
r_spot = d × tan(0.025°) = 3.844e8 × 4.36e-4 ≈ 167,600 m

This is the far-field cross arm half-width — set by the DOE pattern, not pure diffraction.
```

For the telescope aperture, we need diffraction not to blur the cross arm edges:

```
θ_diff = 1.22 × λ / D

Setting θ_diff ≤ 0.05° / 4 = 0.0125° = 2.18e-4 rad:
D ≥ 1.22 × 532e-9 / 2.18e-4 ≈ 0.003 m = 3 mm
```

The diffraction limit is easily met with even a small aperture. We target **D = 0.5–1.0 m** to:
- Keep the central (undiffracted) beam power tight
- Provide structural stability and mounting for the DOE
- Allow future aperture growth for power scaling

### 3.3 Diffractive Optical Element (DOE)

The DOE converts the circular Gaussian output of the telescope into a cross-shaped far-field pattern. It is a computer-generated hologram computed via the Gerchberg-Saxton iterative Fourier algorithm.

**Cross pattern parameters:**

| Parameter | Value |
|---|---|
| Total angular span | 0.7° (matches continental US angular width from Moon) |
| Arm thickness | 0.05° |
| Horizontal arm solid angle | Ω_h = (0.7°)(0.05°) × (π/180)² ≈ 1.06 × 10⁻⁵ sr |
| Vertical arm solid angle | Ω_v ≈ 1.06 × 10⁻⁵ sr |
| Overlap at center | small: ~(0.05°)² ≈ 7.6 × 10⁻⁷ sr |
| Total solid angle | **Ω ≈ 2.05 × 10⁻⁵ sr** |

**DOE efficiency:** A fused-silica surface-relief DOE achieves 80–95% diffraction efficiency into the designed orders. We budget 80% (conservative). 10–20% of power remains in the undiffracted zero-order beam; this must be blocked or directed away from Earth.

The Gerchberg-Saxton algorithm is already prototyped in `prototype/doe_pattern.py`.

### 3.4 Radiometric Power Calculation

The required irradiance at Earth for naked-eye visibility of a green source against the night sky:

```
E_min ≈ 1 × 10⁻⁹ W/m²
(bright, unmistakable — comparable to magnitude 0 star)
```

**Required optical power:**

```
P_opt = E × Ω × d²

d² = (3.844 × 10⁸ m)² = 1.477 × 10¹⁷ m²

P_opt = (1 × 10⁻⁹ W/m²) × (2.05 × 10⁻⁵ sr) × (1.477 × 10¹⁷ m²)
      = 3.0 kW optical (minimum, for solid cross)
      → 5 kW with margin
```

**Electrical power:**

```
P_elec = P_opt / η_wall-plug = 5,000 W / 0.35 ≈ 14.3 kW
```

Budget at **15 kW** electrical for the laser subsystem.

---

## 4. Power System

### 4.1 Landing Site: Peak of Eternal Light

The lunar north pole has several elevated ridges and crater rims that receive near-continuous solar illumination. The rim of Peary crater (~88.6°N) and ridges near Whipple crater are primary candidates. These sites receive sunlight 70–95% of the time, with eclipse periods of hours at most during lunar winter.

**Solar constant at Moon:** 1,361 W/m² (same as Earth, no atmosphere)

### 4.2 Solar Array: Rocket Lab (SolAero) IMM-α

Operating in vacuum with no weather or oxidation, we use **bare** IMM-α (inverted metamorphic multi-junction) cells mounted on lightweight Kapton substrate — no glass cover sheet required. These cells are manufactured by Rocket Lab Space Systems, which acquired SolAero Technologies in 2022. They are the same cell technology used in high-performance satellite power systems and are commercially available through Rocket Lab's established procurement path.

| Parameter | Value |
|---|---|
| Technology | SolAero IMM-α, bare cells on Kapton film |
| Cell efficiency | 33% (AM0, beginning of life) |
| Areal density | 2 kg/m² deployed (no cover glass, lightweight substrate) |
| Panel output density | 1,361 × 0.33 = 449 W/m² |
| Deployment | Rollout panels unfurling from Starship hull exterior |

```
Required electrical power: ~17 kW (laser + avionics + thermal + margin)
Panel output density: 1,361 × 0.33 = 449 W/m²
Required area: 17,000 / 449 ≈ 37.9 m²
```

**Baseline:** 45 m² → **~20 kW peak output** (margin for degradation)  
**Mass:** 45 m² × 2 kg/m² = **90 kg** (vs. 500 kg with traditional panels)

**Upgrade path:** Rocket Lab's next-generation **IMM-β** cell achieves 33.3% efficiency with improved specific power (W/kg). It is a drop-in replacement for IMM-α requiring no redesign of the array structure or power system. If available at mission procurement time, IMM-β would provide additional degradation margin at no mass penalty.

### 4.3 Battery Technology: Amprius Silicon-Anode

We baseline **Amprius SiCore** silicon-anode lithium-ion cells — the highest energy-density Li-ion cells commercially available. Amprius already ships to aerospace and defense customers (including HAPS platforms).

| Level | Energy density | Notes |
|---|---|---|
| Cell | 400 Wh/kg | Amprius SiCore, shipping commercially |
| Pack (custom vacuum-rated) | ~280 Wh/kg | 70% cell-to-pack ratio; no liquid cooling (vacuum radiative only), lightweight composite enclosure, BMS |

### 4.4 Battery Sizing (Eclipse Bridging)

Longest eclipse at polar peaks: estimated 12–72 hours during worst-case lunar winter. The laser shuts down during eclipses (no nighttime visibility anyway — if the Moon is eclipsed from Earth's perspective, it's not visible). Battery sized for avionics + thermal survival only:

```
Required energy: 1 kW × 72 hr = 72 kWh usable
Depth of discharge (80% for cycle life): 72 / 0.80 = 90 kWh capacity
At 280 Wh/kg pack-level (Amprius):
Mass = 90,000 / 280 = 321 kg
```

**Baseline:** 325 kg Amprius silicon-anode battery bank.

### 4.5 Power Budget

| Subsystem | Power (W) | Notes |
|---|---|---|
| Laser (optical 5 kW @ 35%) | 14,300 | Dominant load |
| Pointing/gimbal | 200 | Low power servo drives |
| Avionics + comms | 300 | Housekeeping, telemetry |
| Thermal heaters | 500 | Keep laser at operating temp during cold |
| Margin (10%) | 1,530 | — |
| **Total** | **16,830 W** | **~17 kW** |

---

## 5. Thermal Management

### 5.1 Waste Heat

```
Waste heat = P_elec - P_opt = 14,300 - 5,000 = 9,300 W ≈ 9.3 kW
```

Additional avionics waste heat: ~0.5 kW  
**Total to reject:** ~10 kW

### 5.2 Radiator Sizing

In lunar vacuum, heat rejection is purely radiative (Stefan-Boltzmann):

```
Q = ε × σ × A × (T_rad⁴ - T_env⁴)

σ = 5.67 × 10⁻⁸ W/m²K⁴
ε = 0.85 (black anodized aluminum)
T_rad = 340 K (operating, ~67°C — reasonable for electronics)
T_env = 100 K (lunar polar night sky background, conservative)

Q/A = 0.85 × 5.67e-8 × (340⁴ - 100⁴)
     = 0.85 × 5.67e-8 × (1.34e10 - 1.0e8)
     = 0.85 × 5.67e-8 × 1.33e10
     ≈ 640 W/m²

Required area: 10,000 / 640 ≈ 15.6 m²
```

**Baseline:** 20 m² radiator panels, mounted flush on the Starship hull exterior.

Starship's stainless steel structure (~200+ tonnes) provides a substantial thermal buffer, stabilising the laser's operating temperature and reducing transient thermal stress. Hull-mounted radiators are simpler and lighter than freestanding deployable panels: no deployment mechanism required, and the hull provides structural support.

---

## 6. Structural & Mass Budget

| Subsystem | Mass (kg) | Basis |
|---|---|---|
| Fiber laser assembly | 250 | IPG YLS class, space-qualified |
| DOE + beam optics (telescope, mounts) | 200 | 0.5 m aperture, lightweight mirror |
| Solar array (45 m², SolAero IMM-α) | 90 | 2 kg/m², bare cells on Kapton, no cover glass |
| Battery bank (Amprius Si-anode) | 325 | 90 kWh @ 280 Wh/kg pack-level |
| Radiator panels (20 m², hull-mounted) | 100 | Flush on Starship hull, no deployment mechanism |
| Pointing assembly (gimbal on boom) | 100 | Star tracker + 2-axis gimbal |
| Avionics + comms | 40 | Minimal custom; shares Starship comms |
| Deployable boom (3–5 m) | 75 | Carbon composite + gimbal interface |
| ~~Structure + pallet~~ | ~~0~~ | **Eliminated — Starship IS the structure** |
| Integration margin (15%) | 177 | — |
| **Total** | **1,357 kg** | **~1.4 tonnes** |

The Starship-integrated architecture reduces total payload mass by **41%** vs. the standalone pallet design (2,306 → 1,357 kg). The payload is a small fraction of Starship's lunar delivery capacity.

---

## 7. Landing & Deployment

### 7.1 Landing Site

**Target:** Peak of eternal light on the rim of Peary crater (88.6°N, ~33°W) or an adjacent ridgeline with confirmed >70% solar illumination, identified from NASA LRO illumination maps.

**Landing system:** SpaceX Starship HLS, using terrain-relative navigation (TRN) for meter-scale precision landing. Starship is not an intermediate step — it is the permanent installation. After touchdown, the landing engines shut down and Starship never departs.

**Height advantage:** With the laser system at ~50 m (top of Starship), the geometric line-of-sight to the horizon is:

```
d_horizon = √(2 × R_Moon × h) = √(2 × 1,737,400 × 50) ≈ 13.2 km
```

This comfortably clears local terrain features, reducing sensitivity to the exact landing spot within the polar region.

### 7.2 Deployment Sequence

1. Starship lands at polar peak (pre-surveyed via LRO); engines shut down permanently
2. SolAero solar panels unfurl from hull exterior; battery begins charging
3. System boots from Starship power bus; self-check and Earth comm link established
4. Pointing system initializes: star tracker acquires attitude, JPL ephemeris loaded
5. Deployable boom extends from Starship nosecone area; laser/optics at operational position
6. Laser fires at 10% power; Earth ground station confirms pointing and cross pattern
7. Full-power commissioning; cross confirmed visible
8. **First Light** — system hands off to autonomous Sunday operation schedule

**Commissioning timeline:** 2–4 weeks post-landing.

### 7.3 Long-Term Structural Durability

Starship's 304L stainless steel hull is well-suited to permanent lunar deployment:
- No corrosion (no oxygen, no moisture)
- Mild polar thermal cycling (~50 K variation vs. 300 K at equatorial sites)
- No wind, seismic, or weather loading
- Design life exceeds mission life by a large margin

---

## 8. Pointing & Tracking

### 8.1 Requirement

The beam must keep the cross centered on the continental US (approximately 38°N, 97°W geographic center) as:
- The Moon orbits Earth (27.3-day period)
- Earth rotates (24-hour period)
- The Moon librates (±6.7° in latitude, ±7.6° in longitude over ~27 days)

**Pointing tolerance:** The cross arm width is 0.7°, so the center must stay within ±0.2° of the target. This is a generous requirement — typical spacecraft pointing systems achieve < 0.1° with star trackers.

### 8.2 System

| Component | Heritage |
|---|---|
| Star tracker | Jena-Optronik Astro APS or equivalent; < 5 arcsec accuracy |
| 2-axis gimbal or reaction wheel | Laser mounted on gimbal; slew rate < 0.01°/s needed |
| Ephemeris computer | Pre-loaded JPL DE430 ephemeris + real-time corrections via uplink |
| Pointing update rate | 1 Hz (Earth moves ~0.004°/s in lunar sky — trivially slow) |

From the lunar north pole, Earth remains near the horizon at all times (0° ± 6.7° elevation with libration). The boom-mounted gimbal therefore points roughly **horizontally**, which simplifies the gimbal design (no need for large elevation range) and ensures the beam clears the Starship hull and any nearby terrain. No real-time human intervention required; the system is fully autonomous.

---

## 9. Visibility Analysis

### 9.1 When Can the Cross Be Seen?

Three conditions must all be met:
1. **Moon above US horizon** — the Moon rises and sets daily
2. **It is night** in the observer's location (cross visible against dark sky)
3. **Moon is full or nearly full** — cross is brightest against the unlit sky around it; crescent Moon phases still work but sky must be dark

### 9.2 Lunar Phase & North Pole Visibility

The laser is at the north pole of the Moon. From Earth, the north pole of the Moon faces us at an angle that varies with **lunar libration** in latitude. Libration in latitude oscillates ±6.7°, meaning the north pole tilts toward Earth by up to 6.7° and away by 6.7° over ~27 days.

- **Maximum north pole visibility:** When libration tilts the north pole toward Earth — the cross projector has the clearest line of sight and the cross appears most symmetric
- **Minimum visibility:** When north pole tilts away — the cross appears foreshortened but the beam geometry is unchanged; the cross still covers the US

### 9.3 Monthly Visible Hours (Approximate)

For a US observer (mid-latitude, ~38°N):

| Moon Phase | Moon above horizon at night | Cross visible? | Hours/month |
|---|---|---|---|
| Full Moon | ~6 hrs/night × ~3 nights | Best visibility | ~18 hrs |
| Waxing/waning gibbous | ~4–8 hrs/night × ~4 nights | Good | ~24 hrs |
| Quarter | ~4 hrs/night × ~2 nights | Marginal (competing sky brightness) | ~8 hrs |
| Crescent | < 2 hrs/night | Poor (twilight) | minimal |
| **Total per month** | — | — | **~30–50 hrs** |

The cross is most spectacular at or near full Moon when 330 million Americans can look up simultaneously.

### 9.4 Seasonal Variation

Winter nights are longer — more viewing hours per month in November–February for northern US observers. The Moon's declination varies ±28.5° over 18.6 years (Metonic-related), but month-to-month the visibility is broadly consistent.

### 9.5 Sunday Operation Mode

The baseline design supports continuous autonomous operation, but the cross fires **only on Sundays** — when the Moon is visible at night over the US. This is a scheduling decision, not a hardware redesign: the same 45 m² SolAero array and 325 kg battery are retained.

**Why not shrink the solar array for Sunday-only duty?**

One might propose a smaller array (~7 m²) that charges a larger battery all week, discharging on Sunday. With SolAero panels at 2 kg/m², the baseline wins decisively:

```
Small solar + burst battery:
  Sunday laser burst: 17 kW × 8 hr = 136 kWh
  With 80% DoD and 90% round-trip efficiency: 136 / (0.80 × 0.90) = 189 kWh
  Battery mass at 280 Wh/kg pack: 189,000 / 280 = 675 kg
  Small solar array (7 m² SolAero): 7 × 2 = 14 kg
  Total: 689 kg

vs. baseline:
  Solar array (45 m² SolAero): 45 × 2 = 90 kg
  Survival battery: 325 kg
  Total: 415 kg
```

The baseline is **274 kg lighter** — the opposite of a wash. SolAero's low areal density (2 kg/m²) makes large arrays cheap on mass, so the week-long charging strategy no longer has a mass incentive. It also adds single-point failure risk and deep cycling stress. Baseline hardware is kept as-is.

**Benefits of Sunday-only operation:**

| Benefit | Impact |
|---|---|
| Laser lifetime | ~416 hrs/year vs 8,760 → effectively indefinite (>240 years at rated 100,000 hrs) |
| Thermal cycling | Reduced stress on optics and laser diodes |
| Ground operations | Monitor Sundays only → saves ~$5–10M over 10-year mission |
| Narrative resonance | The cross appears on the Sabbath; Easter Sunday is the natural inaugural event |

---

## 10. Cost Estimates (Order of Magnitude)

All figures in 2025 USD. Ranges reflect uncertainty from COTS-to-space-qualified premium (typically 5–20×).

### 10.1 Core Project (projector, energy system, Starship modifications)

| Item | Low ($M) | High ($M) | Basis |
|---|---|---|---|
| Laser system (5 kW, space-qualified) | 5 | 15 | Commercial fiber lasers ~$200–500/W; space-qual premium |
| DOE + beam optics | 2 | 5 | Custom fused-silica DOE + 0.5 m telescope |
| Solar array (45 m², SolAero IMM-α) | 5 | 12 | Premium bare cells; less area, similar total cost |
| Battery bank (Amprius Si-anode) | 3 | 8 | 325 kg; COTS cells + custom space pack |
| Radiators + thermal (hull-mounted) | 1 | 2 | Simpler integration vs. freestanding panels |
| Pointing assembly + boom | 3 | 8 | Boom + gimbal + star tracker |
| Avionics + comms | 1 | 3 | Minimal custom; shares Starship infrastructure |
| Starship integration (mods + interfaces) | 3 | 8 | Hull/power/comms integration with SpaceX |
| System integration & test | 8 | 20 | Environmental testing (thermal-vac, vibration) |
| Ground station setup | 3 | 8 | Antenna, control software |
| Project management + contingency | 8 | 25 | 15–20% of hardware cost |
| **Core project subtotal** | **42** | **114** | **without launch** |

### 10.2 Launch & Delivery

| Item | Low ($M) | High ($M) | Basis |
|---|---|---|---|
| Starship lunar cargo flight | 20 | 50 | SpaceX projected lunar cargo pricing |

**Grand total (core + launch): $62–164M**

The core project — the projector, energy system, and Starship modifications — costs **$42–114M**. Launch is a separable line item: if the hardware rides as manifested cargo on a Starship flight that is flying anyway, the incremental launch cost is zero. Even paying for a dedicated flight, the complete mission fits within the budget of a medium-class space mission.

**For comparison:** The Hubble Space Telescope cost ~$1.5B (1990 dollars). A single NASA CLPS lunar lander contract costs $100–400M. Stellar Dominion is achievable for the cost of one CLPS contract — and would be seen by orders of magnitude more people.

---

## 11. Operational Lifetime & Costs

### 11.1 Component Lifetimes

| Component | Rated life | Notes |
|---|---|---|
| Fiber laser | 100,000+ hours (~11 years continuous) | IPG rated; Sunday-only: ~416 hrs/yr → effectively indefinite |
| Solar array | 15–20 years | Radiation degradation ~1–3%/year at lunar orbit |
| Amprius Si-anode battery | 1,000–2,000 cycles | Sunday-only cycling extends life well beyond 10 years |
| Avionics | 10–15 years | Rad-hard components |
| DOE (passive optic) | Indefinite | No moving parts, no degradation in vacuum |
| Pointing gimbal | 7–10 years | Wear item; can be oversized for longer life |

**Mission design life: 10 years** (Sunday-only operation — laser and battery lifetimes are not the limiting factor)

### 11.2 Annual Operating Costs (Sunday Operation Mode)

| Item | $/year | Notes |
|---|---|---|
| Ground station operations | 500,000–1,500,000 | Sunday monitoring + weekly health checks |
| Mission operations team | 300,000–800,000 | 1–3 FTE (highly autonomous; Sunday operations cadence) |
| Ephemeris updates + uplink | 50,000–200,000 | — |
| Contingency | 150,000–300,000 | — |
| **Annual total** | **~$1.0–2.8M** | — |

**10-year total operating cost:** ~$10–28M  
**Core project + 10 years ops (no launch):** ~$52–142M  
**Full lifecycle (core + Starship flight + 10 years ops):** ~$72–192M

---

## 12. Regulatory Notes

A full regulatory analysis is beyond the scope of this document; key touchpoints:

- **Outer Space Treaty (1967), Article II:** Prohibits national appropriation of the Moon. Private installations for peaceful purposes are not prohibited; the 2015 SPACE Act and analogous legislation confirm US companies can own hardware on celestial bodies.
- **Laser safety:** At Earth, the cross irradiance (~1 × 10⁻⁹ W/m²) is orders of magnitude below ANSI Z136.1 MPE for extended-source viewing. The beam is eye-safe for diffuse viewing.
- **Aviation:** FAA NOTAMs and precise ephemeris-based aiming ensure the beam does not intersect aircraft corridors within the US Class A airspace volume (beam enters from above).
- **ITAR/EAR:** Multi-kW lasers are controlled items; export license required for the hardware. Standard for aerospace programs.
- **ITU coordination:** No radio-frequency spectrum coordination needed (optical wavelength, not RF).

---

## 13. Project Timeline — Easter 2027 Target

**Aspirational first-light: Easter Sunday, April 1, 2027.**

Working backward from Easter 2027:
- First Light: April 1, 2027
- Landing + commissioning (2–4 weeks): launch by early March 2027
- Lunar transit (~4 days): depart Earth late February 2027
- Payload integration with Starship: complete mid-February 2027
- Available build time from April 2026: **~10 months**

This is a compressed schedule (10 months vs. 12-month baseline). Compression is achieved by: ordering the laser immediately at kickoff (Month 0), overlapping integration with late hardware deliveries, and running thermal-vacuum and vibration tests in parallel.

| Milestone | Month | Key deliverables |
|---|---|---|
| Project kickoff + laser order | 0 | Requirements baseline, team assembly, laser ordered immediately |
| PDR (Preliminary Design Review) | 1.5 | System architecture frozen |
| DOE fabrication begins | 2 | Final GS pattern → fused-silica vendor |
| Solar array + battery delivery | 2–5 | Amprius cells + custom pack, space-grade solar |
| CDR (Critical Design Review) | 4 | Detailed design complete |
| System integration begins | 5 | Integration overlaps with late deliveries |
| Thermal-vacuum + vibration (parallel) | 6–8 | Compressed env test campaign |
| Starship payload integration | 8 | Subsystems installed and verified in Starship |
| Launch readiness review | 9 | All tests passed, launch authorization |
| **Launch-ready** | **10** | Ready for Starship lunar cargo flight |
| Landing + commissioning | L+0 to L+30 days | Deploy, commission, confirm cross from Earth |
| **First Light** | **Easter Sunday** | **April 1, 2027** |

**Schedule compression cost premium:** +$8–20M (overtime, parallel work streams, expedited shipping, higher contingency).

**Hard dependency: Starship HLS availability.** The gating item is not our build but whether SpaceX is flying lunar cargo by early 2027. If Starship is not available, the Easter 2027 target is not achievable regardless of our readiness. This dependency is acknowledged honestly; the 10-month build ensures we are ready the moment Starship is.

---

## 14. References

- NASA Lunar Fact Sheet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
- LRO Illumination Maps (peaks of eternal light): NASA GSFC / LROC team
- Continental US dimensions: USGS / Wikipedia "Geography of the United States"
- IPG Photonics YLS series product literature (multi-kW CW fiber lasers)
- nLIGHT product literature
- Lunar ISRU & Artemis program: NASA HQ / Marshall Space Flight Center
- Radiometry: Boyd, R. W., *Radiometry and the Detection of Optical Radiation*, Wiley
- Night-sky visibility thresholds: amateur astronomy references & ANSI Z136.6
- Gerchberg-Saxton algorithm: Gerchberg, R.W. & Saxton, W.O. (1972), *Optik* 35, 237
- NASA Kilopower / KRUSTY reactor: Gibson, M.A. et al. (2018), *Nuclear Technology*
- Amprius Technologies: SiCore silicon-anode cell product data (400 Wh/kg cell-level)
- Rocket Lab Space Systems (formerly SolAero Technologies): IMM-α and IMM-β inverted metamorphic multi-junction solar cell data; https://www.rocketlabusa.com/space-systems/solar/
- SpaceX Starship HLS: NASA CPS contract documentation
- Outer Space Treaty (1967): UN Office for Outer Space Affairs
- SPACE Act (2015): 51 U.S.C. § 51303
