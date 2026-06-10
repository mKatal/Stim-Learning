import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import stim


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

CSV_PATH = RESULTS_DIR / "detector_sampling_sweep.csv"


def run_single_experiment(
    distance: int,
    rounds: int,
    noise: float,
    shots: int,
) -> dict:
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=noise,
    )

    sampler = circuit.compile_detector_sampler()

    detector_events, logical_observables = sampler.sample(
        shots=shots,
        separate_observables=True,
    )

    total_detector_events = int(detector_events.sum())
    detector_event_rate = total_detector_events / (
        shots * circuit.num_detectors
    )

    detector_events_per_shot = detector_events.sum(axis=1)
    average_detector_events_per_shot = float(
        np.mean(detector_events_per_shot)
    )

    logical_flips = int(logical_observables.sum())
    logical_flip_rate = logical_flips / shots

    return {
        "distance": distance,
        "rounds": rounds,
        "noise": noise,
        "shots": shots,
        "num_qubits": circuit.num_qubits,
        "num_detectors": circuit.num_detectors,
        "num_observables": circuit.num_observables,
        "total_detector_events": total_detector_events,
        "detector_event_rate": detector_event_rate,
        "average_detector_events_per_shot": average_detector_events_per_shot,
        "logical_flips": logical_flips,
        "logical_flip_rate": logical_flip_rate,
    }


def run_parameter_sweep() -> list[dict]:
    distances = [3, 5, 7]
    rounds_list = [3, 5, 7, 9]
    noise_values = [0.001, 0.003, 0.01, 0.1]
    shots = 10000

    results = []

    total_runs = (
        len(distances)
        * len(rounds_list)
        * len(noise_values)
    )

    run_index = 1

    for distance in distances:
        for rounds in rounds_list:
            for noise in noise_values:
                print(
                    f"Run {run_index}/{total_runs}: "
                    f"d={distance}, rounds={rounds}, noise={noise}"
                )

                result = run_single_experiment(
                    distance=distance,
                    rounds=rounds,
                    noise=noise,
                    shots=shots,
                )

                results.append(result)
                run_index += 1

    return results


def save_results_to_csv(results: list[dict]) -> None:
    if not results:
        return

    with open(CSV_PATH, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved results to: {CSV_PATH}")


def plot_noise_vs_detector_events(results: list[dict]) -> None:
    plt.figure()

    for distance in sorted({r["distance"] for r in results}):
        xs = []
        ys = []

        for result in results:
            if (
                result["distance"] == distance
                and result["rounds"] == 5
            ):
                xs.append(result["noise"])
                ys.append(result["average_detector_events_per_shot"])

        plt.plot(xs, ys, marker="o", label=f"distance {distance}")

    plt.xlabel("Physical noise probability")
    plt.ylabel("Average detector events per shot")
    plt.title("Noise vs detector events")
    plt.legend()
    plt.grid(True)

    output_path = RESULTS_DIR / "noise_vs_detector_events.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def plot_noise_vs_logical_flips(results: list[dict]) -> None:
    plt.figure()

    for distance in sorted({r["distance"] for r in results}):
        xs = []
        ys = []

        for result in results:
            if (
                result["distance"] == distance
                and result["rounds"] == 5
            ):
                xs.append(result["noise"])
                ys.append(result["logical_flip_rate"])

        plt.plot(xs, ys, marker="o", label=f"distance {distance}")

    plt.xlabel("Physical noise probability")
    plt.ylabel("Logical flip rate")
    plt.title("Noise vs logical flips")
    plt.legend()
    plt.grid(True)

    output_path = RESULTS_DIR / "noise_vs_logical_flips.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def plot_rounds_vs_detector_events(results: list[dict]) -> None:
    plt.figure()

    for noise in sorted({r["noise"] for r in results}):
        xs = []
        ys = []

        for result in results:
            if (
                result["distance"] == 3
                and result["noise"] == noise
            ):
                xs.append(result["rounds"])
                ys.append(result["average_detector_events_per_shot"])

        plt.plot(xs, ys, marker="o", label=f"noise {noise}")

    plt.xlabel("Syndrome extraction rounds")
    plt.ylabel("Average detector events per shot")
    plt.title("Rounds vs detector events, distance 3")
    plt.legend()
    plt.grid(True)

    output_path = RESULTS_DIR / "rounds_vs_detector_events.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_summary(results: list[dict]) -> None:
    print("\n=== SUMMARY ===")

    for result in results:
        print(
            "d=",
            result["distance"],
            "| rounds=",
            result["rounds"],
            "| noise=",
            result["noise"],
            "| avg detector events/shot=",
            round(result["average_detector_events_per_shot"], 3),
            "| logical flip rate=",
            round(result["logical_flip_rate"], 4),
        )


def main() -> None:
    results = run_parameter_sweep()

    save_results_to_csv(results)
    print_summary(results)

    plot_noise_vs_detector_events(results)
    plot_noise_vs_logical_flips(results)
    plot_rounds_vs_detector_events(results)

    print("\nDone.")


if __name__ == "__main__":
    main()