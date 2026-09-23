# dem-sph

A minimal build of [miluphcuda](https://github.com/christophmschaefer/miluphcuda), a 3D CUDA Smoothed Particle
Hydrodynamics (SPH) code for astrophysical collision and impact processes, kept lean for DEM/SPH experimentation.

This repo intentionally omits miluphcuda's `examples/`, `test_cases/`, and `doc/` — only what's needed to build and
run the code, plus pre/post-processing utilities, is included.

## Layout

* `src/`, `include/` — miluphcuda source and headers
* `Makefile`, `configure.sh` — build
* `material-config/` — material config file format (`CREATE-MATERIAL-CONFIG.md`) and a library of material parameters
* `pc_values.dat` — runtime lookup table read by `io.cu`
* `utils/preprocessing/`, `utils/postprocessing/` — scripts for generating initial conditions and analyzing output

## Owners

Sfair & Gomes (2026)

## Reference

For full documentation, examples, and test cases, see the upstream
[miluphcuda repository](https://github.com/christophmschaefer/miluphcuda).
