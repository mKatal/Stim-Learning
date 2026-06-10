# Stim Learning

This repository is a long-term learning project focused on quantum error correction software using [Stim](https://github.com/quantumlib/Stim).

The purpose of this repository is not to present a finished software package, but to document my gradual learning process. I use this space to understand how stabilizer-circuit simulation, detector-event sampling, decoding, and surface-code experiments work in practice.

The repository is intentionally organized into separate folders, where each folder represents a small, self-contained workflow or experiment. Early folders are minimal and educational; later folders are expected to become more structured and closer to realistic QEC software workflows.

This project is a work in progress and may remain under construction indefinitely. I expect to keep revisiting, rewriting, and expanding parts of it as my understanding of QEC software improves.

## Motivation

My current goal is to build practical familiarity with:

- Stim-based stabilizer-circuit simulation
- detector events and logical observables
- surface-code memory experiments
- syndrome sampling
- decoder integration, starting with PyMatching
- visualization of QEC data
- hardware-inspired noise models
- selected scenarios inspired by experimental QEC work with superconducting circuits

The longer-term direction is to implement and study small software experiments inspired by the QEC scenarios discussed in Nathan Lacroix's PhD thesis, *Quantum Error Correction with Superconducting Circuits*.

# 00 Stim Minimal

A first minimal experiment with Stim.

This script generates a small noisy rotated surface-code memory circuit, samples detector events and logical observables, and prints a simple summary of what happened in each shot.

The purpose is to understand Stim’s basic workflow before adding decoding, visualization, or more advanced QEC experiments.

# 01 Detector Sampling Sweep

This workflow focuses on detector-event statistics before introducing decoding.

The script runs automated Stim simulations for different surface-code parameters and collects basic statistics about detector events and logical observable flips. It is intended to build intuition for how noisy QEC circuits behave before asking a decoder to interpret the syndrome data.

For each configuration, the script records quantities such as:

* number of qubits,
* number of detectors,
* total detector events,
* average detector events per shot,
* logical flip rate.

The purpose of this step is to understand the relationship between physical noise, syndrome activity, and logical observable flips.

No decoder is used in this workflow. Stim only generates the noisy samples and reports the detector events and logical observables. This keeps the experiment focused on understanding what Stim produces directly.

# 02 PyMatching Minimal

This is the first minimal decoding experiment in the repository.

The script generates a small noisy rotated surface-code memory circuit using Stim, converts the circuit into a detector error model, and builds a PyMatching decoder from that model.

Stim samples detector events and true logical observable flips. PyMatching receives only the detector events and predicts the logical observable flips. The script then compares PyMatching’s predictions with Stim’s hidden ground truth.

This introduces the basic decoding pipeline:

```text
Stim circuit
    → detector error model
    → PyMatching decoder
    → predicted logical observables
    → comparison with true logical observables
```

The key idea is that the detector events are the information available to the decoder, while the true logical observables are only available because this is a simulation.

This script is intentionally small and direct. Its purpose is to make the decoding workflow understandable before moving on to parameter sweeps, visualization, or custom decoder experiments.

# 03 Decoding Sweep

This workflow extends the basic PyMatching example into an automated decoding experiment.

The script generates noisy rotated surface-code memory circuits with different distances, syndrome-extraction rounds, and physical noise values. For each configuration, Stim samples detector events and true logical observables. PyMatching then decodes the detector events and predicts the logical observable flips.

The main quantity of interest is the **decoder failure rate**, which measures how often PyMatching’s prediction disagrees with Stim’s hidden ground truth.

This step is useful for building intuition about how decoding performance changes with:

* physical noise probability,
* code distance,
* number of syndrome-extraction rounds,
* average number of detector events per shot.

The script also saves the collected sweep data as a CSV file and creates simple plots for visual inspection.

At this stage, PyMatching is used as a baseline decoder. The goal is not yet to implement a custom decoder, but to understand the standard Stim → detector error model → PyMatching workflow.


## Reference Material

This learning project is partly inspired by selected scenarios from:

Nathan Lacroix, *Quantum Error Correction with Superconducting Circuits*, Doctoral Thesis, ETH Zurich, 2025.  
DOI: https://doi.org/10.3929/ethz-b-000740393
