"""Generate one synthetic laser-heating run: temperature of saltwater over time.

Model: T(t) = start_temp + HEATING_COEFF * power * t + Gaussian noise

Usage:
    python generate_measurement.py --power 30 --material granite
    python generate_measurement.py --power 30 --material granite --out ../output_data/measurement.csv
"""

import argparse
import csv
import random
from pathlib import Path

HEATING_COEFF = 0.002  # degC per (W * s)
NOISE_SD = 0.15  # degC


def generate(
    power_w,
    start_temp=20.0,
    break_temp=None,
    duration_s=120.0,
    step_s=0.5,
    seed=None,
):
    """Return a list of (time_s, temperature_C) rows."""
    # Same power gives the same data unless a seed is given explicitly.
    rng = random.Random(power_w if seed is None else seed)
    n = int(duration_s / step_s) + 1
    rows = []
    for i in range(n):
        t = i * step_s
        temp = (
            start_temp + HEATING_COEFF * power_w * t + rng.gauss(0, NOISE_SD)
        )
        rows.append((round(t, 2), round(temp, 3)))
        if temp == break_temp:
            break
    return rows


def generate_measurement(
    power_w,
    start_temp=20.0,
    break_temp=None,
    duration_s=120.0,
    step_s=0.5,
    seed=None,
    output_path=None,
):
    rows = generate(
        power_w=power_w,
        start_temp=start_temp,
        break_temp=break_temp,
        duration_s=duration_s,
        step_s=step_s,
        seed=seed,
    )

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time_s", "temperature_C"])
            writer.writerows(rows)

    return rows
