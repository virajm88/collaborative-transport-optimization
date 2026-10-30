"""Reproduce the main study, sensitivity analysis and multi-seed benchmark."""

from pathlib import Path

from collab_transport.data import generate_instance
from collab_transport.experiments import benchmark, run_study, sensitivity


def main() -> None:
    output = Path("outputs")
    instance = generate_instance(seed=42)
    print("Running main study...", flush=True)
    summary = run_study(instance, output / "demo")
    print(f"Modelled savings: {summary['savings_pct']:.2f}%", flush=True)
    print("Running 9 sensitivity scenarios...", flush=True)
    sensitivity(instance, output / "sensitivity")
    print("Running 9 benchmark instances...", flush=True)
    benchmark(output / "benchmark", [6, 12, 24], [4, 6, 8], [7, 42, 101])
    print("Finished. Read outputs/demo/report.md.", flush=True)


if __name__ == "__main__":
    main()

