import stim


# 1. Create a tiny generated surface-code circuit.
circuit = stim.Circuit.generated(
    "surface_code:rotated_memory_x",
    distance=3,
    rounds=3,
    after_clifford_depolarization=0.001,
)

print("=== CIRCUIT ===")
print(circuit)


# 2. Ask Stim how many detectors and logical observables exist.
print("\n=== CIRCUIT INFO ===")
print("number of qubits:", circuit.num_qubits)
print("number of detectors:", circuit.num_detectors)
print("number of observables:", circuit.num_observables)


# 3. Compile a detector sampler.
sampler = circuit.compile_detector_sampler()


# 4. Take a few samples.
shots = 100_000
samples = sampler.sample(
    shots=shots,
    separate_observables=True,
)

detector_events, logical_observables = samples


print("\n=== DETECTOR EVENTS ===")
print(detector_events.astype(int))

print("\n=== LOGICAL OBSERVABLES ===")
print(logical_observables.astype(int))


count_observable_errors = 0
for observable_error in logical_observables:
    if observable_error ==  True:
        count_observable_errors +=1

print("\n=== LOGICAL OBSERVABLE ERROR RATE ===")        
print(count_observable_errors/shots)


# 5. Summarize what happened.
if False:
    print("\n=== SIMPLE SUMMARY ===")

    total_detector_events = detector_events.sum()
    logical_failures = logical_observables.sum()

    print("total detector events:", total_detector_events)
    print("logical failures:", logical_failures)

    print("\nPer shot:")

    for shot_index in range(shots):
        detector_count = detector_events[shot_index].sum()
        logical_flip = logical_observables[shot_index][0]
        if logical_flip:

            print(
                "shot",
                shot_index,
                "| detector events:",
                detector_count,
                "| logical flip:",
                int(logical_flip),
            )