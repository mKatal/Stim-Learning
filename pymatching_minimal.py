import numpy as np
import stim
import pymatching


# 1. Create noisy surface-code memory circuit.
circuit = stim.Circuit.generated(
    "surface_code:rotated_memory_x",
    distance=7,
    rounds=3,
    after_clifford_depolarization=0.001,
)

print("=== CIRCUIT INFO ===")
print("number of qubits:", circuit.num_qubits)
print("number of detectors:", circuit.num_detectors)
print("number of logical observables:", circuit.num_observables)


# 2. Convert Stim circuit into a detector error model.
#
# This model tells the decoder:
# - which physical errors can flip which detectors
# - which physical errors can flip logical observables
detector_error_model = circuit.detector_error_model(
    decompose_errors=True
)

print("\n=== DETECTOR ERROR MODEL PREVIEW ===")
print(str(detector_error_model)[:1000])
print("...")


# 3. Build PyMatching decoder from Stim's detector error model.
decoder = pymatching.Matching.from_detector_error_model(
    detector_error_model
)


# 4. Sample detector events and true logical observables from Stim.
sampler = circuit.compile_detector_sampler()

shots = 100_000

detector_events, true_logical_observables = sampler.sample(
    shots=shots,
    separate_observables=True,
)


# 5. Let PyMatching predict logical flips from detector events.
predicted_logical_observables = decoder.decode_batch(detector_events)


# 6. Compare prediction with truth.
#
# If prediction != true logical observable,
# then the decoder failed for that shot.
decoder_failures = np.any(
    predicted_logical_observables != true_logical_observables,
    axis=1,
)

number_of_failures = int(np.sum(decoder_failures))
decoder_failure_rate = number_of_failures / shots


print("\n=== DECODING RESULTS ===")
print("shots:", shots)
print("decoder failures:", number_of_failures)
print("decoder failure rate:", decoder_failure_rate)


'''print("\n=== FIRST 10 SHOTS ===")

for shot_index in range(10):
    detector_count = int(detector_events[shot_index].sum())
    true_flip = int(true_logical_observables[shot_index][0])
    predicted_flip = int(predicted_logical_observables[shot_index][0])
    failed = bool(decoder_failures[shot_index])
  

    print(
        "shot",
        shot_index,
        "| detector events:",
        detector_count,
        "| true logical flip:",
        true_flip,
        "| predicted logical flip:",
        predicted_flip,
        "| decoder failed:",
        failed,
    )'''

print("\n=== FAILED SHOTS ===")  

for shot_index in range(shots):
    failed = bool(decoder_failures[shot_index])

    if failed:
        detector_count = int(detector_events[shot_index].sum())
        true_flip = int(true_logical_observables[shot_index][0])
        predicted_flip = int(predicted_logical_observables[shot_index][0])


        print(
            "shot",
            shot_index,
            "| detector events:",
            detector_count,
            "| true logical flip:",
            true_flip,
            "| predicted logical flip:",
            predicted_flip,
            "| decoder failed:",
            failed,
        )