import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pymatching
import stim


RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

CSV_PATH = RESULTS_DIR / "decoding_sweep.csv"


def run_single_decoding_experiment(
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

    detector_error_model = circuit.detector_error_model(
        decompose_errors=True
    )

    decoder = pymatching.Matching.from_detector_error_model(
        detector_error_model
    )

    sampler = circuit.compile_detector_sampler()

    detector_events, true_logical_observables = sampler.sample(
        shots=shots,
        separate_observables=True,
    )

    predicted_logical_observables = decoder.decode_batch(
        detector_events
    )

    decoder_failures = np.any(
        predicted_logical_observables != true_logical_observables,
        axis=1,
    )

    number_of_failures = int(np.sum(decoder_failures))
    decoder_failure_rate = number_of_failures / shots

    average_detector_events_per_shot = float(
        np.mean(detector_events.sum(axis=1))
    )

    return {
        "distance": distance,
        "rounds": rounds,
        "noise": noise,
        "shots": shots,
        "num_qubits": circuit.num_qubits,
        "num_detectors": circuit.num_detectors,
        "average_detector_events_per_shot": average_detector_events_per_shot,
        "decoder_failures": number_of_failures,
        "decoder_failure_rate": decoder_failure_rate,
    }


def run_sweep() -> list[dict]:
    distances = [3, 5, 7]
    rounds_list = [3, 5, 7]
    noise_values = [0.001, 0.003, 0.01, 0.1]
    shots = 1_000_000

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

                result = run_single_decoding_experiment(
                    distance=distance,
                    rounds=rounds,
                    noise=noise,
                    shots=shots,
                )

                results.append(result)
                run_index += 1

    return results


def save_results_to_csv(results: list[dict]) -> None:
    with open(CSV_PATH, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved results to: {CSV_PATH}")


def plot_noise_vs_decoder_failure(results: list[dict]) -> None:
    plt.figure()

    fixed_rounds = 5

    for distance in sorted({r["distance"] for r in results}):
        xs = []
        ys = []

        for result in results:
            if (
                result["distance"] == distance
                and result["rounds"] == fixed_rounds
            ):
                xs.append(result["noise"])
                ys.append(result["decoder_failure_rate"])

        plt.plot(xs, ys, marker="o", label=f"distance {distance}")

    plt.xlabel("Physical noise probability")
    plt.ylabel("Decoder failure rate")
    plt.title(f"Noise vs decoder failure rate, rounds={fixed_rounds}")
    plt.legend()
    plt.grid(True)

    output_path = RESULTS_DIR / "noise_vs_decoder_failure_rate.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def plot_rounds_vs_decoder_failure(results: list[dict]) -> None:
    plt.figure()

    fixed_distance = 3

    for noise in sorted({r["noise"] for r in results}):
        xs = []
        ys = []

        for result in results:
            if (
                result["distance"] == fixed_distance
                and result["noise"] == noise
            ):
                xs.append(result["rounds"])
                ys.append(result["decoder_failure_rate"])

        plt.plot(xs, ys, marker="o", label=f"noise {noise}")

    plt.xlabel("Syndrome extraction rounds")
    plt.ylabel("Decoder failure rate")
    plt.title(f"Rounds vs decoder failure rate, distance={fixed_distance}")
    plt.legend()
    plt.grid(True)

    output_path = RESULTS_DIR / "rounds_vs_decoder_failure_rate.png"
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


def print_summary(results: list[dict]) -> None:
    print("\n=== DECODING SWEEP SUMMARY ===")

    for result in results:
        print(
            "d=",
            result["distance"],
            "| rounds=",
            result["rounds"],
            "| noise=",
            result["noise"],
            "| avg detectors/shot=",
            round(result["average_detector_events_per_shot"], 3),
            "| decoder failure rate=",
            round(result["decoder_failure_rate"], 5),
        )


def main() -> None:
    results = run_sweep()

    save_results_to_csv(results)
    print_summary(results)

    plot_noise_vs_decoder_failure(results)
    plot_rounds_vs_decoder_failure(results)

    print("\nDone.")


if __name__ == "__main__":
    main()