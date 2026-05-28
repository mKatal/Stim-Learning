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

## Reference Material

This learning project is partly inspired by selected scenarios from:

Nathan Lacroix, *Quantum Error Correction with Superconducting Circuits*, Doctoral Thesis, ETH Zurich, 2025.  
DOI: https://doi.org/10.3929/ethz-b-000740393
