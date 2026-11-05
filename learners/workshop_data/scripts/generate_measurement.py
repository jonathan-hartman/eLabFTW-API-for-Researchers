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
    power_w, start_temp=20.0, break_temp=None, duration_s=120.0, step_s=0.5, seed=None
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

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--power", type=float, required=True, help="laser power in W"
    )
    parser.add_argument(
        "--start-temp",
        type=float,
        default=20.0,
        help="start temperature in degC",
    )
    parser.add_argument(
        "--duration", type=float, default=120.0, help="run length in s"
    )
    parser.add_argument(
        "--step", type=float, default=0.5, help="sampling interval in s"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="random seed (default: the power value)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("measurement.csv"),
        help="output CSV path",
    )
    args = parser.parse_args()

    rows = generate(
        args.power, args.start_temp, args.duration, args.step, args.seed
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "temperature_C"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
