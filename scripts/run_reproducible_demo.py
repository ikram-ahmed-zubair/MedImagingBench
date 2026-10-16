"""A tiny deterministic run that demonstrates config + metadata capture."""
from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/example.yaml")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    experiment = config["experiment"]
    seed = int(experiment["seed"])
    rng = np.random.default_rng(seed)
    sample = rng.normal(size=1000)

    output_dir = Path(experiment["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "experiment_name": experiment["name"],
        "config_path": str(config_path),
        "seed": seed,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "n_samples": int(sample.size),
        "sample_mean": float(sample.mean()),
        "sample_std": float(sample.std()),
        "note": "Demo only; replace with validated experiment code and add a Git commit SHA.",
    }
    output_file = output_dir / "run_metadata.json"
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote reproducibility metadata to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
