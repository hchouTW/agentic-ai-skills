from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import awkward as ak
import numpy as np
import uproot
import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an uproot plus awkward analysis.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def require_branches(tree: uproot.behaviors.TTree.TTree, branches: list[str]) -> None:
    available = set(tree.keys())
    missing = [branch for branch in branches if branch not in available]
    if missing:
        raise KeyError(f"Missing required branches: {', '.join(missing)}")


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    tree_name = config["inputs"]["tree"]
    input_paths = [Path(path) for path in config["inputs"]["files"]]
    required_branches = config["branches"]["required"]

    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(f"Input file does not exist: {path}")

    arrays = []
    for path in input_paths:
        with uproot.open(path) as root_file:
            if tree_name not in root_file:
                raise KeyError(f"Tree '{tree_name}' not found in {path}")
            tree = root_file[tree_name]
            require_branches(tree, required_branches)
            arrays.append(tree.arrays(required_branches, library="ak"))

    events = ak.concatenate(arrays) if len(arrays) > 1 else arrays[0]
    has_two_muons = events["nMuon"] >= 2
    selected_events = events[has_two_muons]
    mask = (
        (selected_events["Muon_pt"][:, 0] > 25.0)
        & (abs(selected_events["Muon_eta"][:, 0]) < 2.4)
    )

    selected_pt = selected_events["Muon_pt"][:, 0][mask]
    selected_weight = selected_events["event_weight"][mask]

    values, edges = np.histogram(
        ak.to_numpy(selected_pt),
        bins=50,
        range=(0.0, 200.0),
        weights=ak.to_numpy(selected_weight),
    )

    output_dir = Path(config["output"]["directory"])
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / config["output"]["root_file"]
    with uproot.recreate(output_path) as output:
        output["h_leading_muon_pt"] = values, edges

    print(f"processed events: {len(events)}")
    print(f"selected events: {ak.sum(mask)}")
    print(f"hist integral: {float(values.sum())}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
