#!/bin/bash
# Submit from login. Compilation, generation, solver and checks run in SLURM.
#SBATCH --job-name=luiz-areia
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4096
#SBATCH --time=60:00:00
#SBATCH --partition=normal
#SBATCH --qos=gpu
#SBATCH --gres=gpu:a40:1
#SBATCH --chdir=/clusteruy/home03/esys/luiz.gomes/miluphcuda
#SBATCH --output=/clusteruy/home03/esys/luiz.gomes/miluphcuda/.cluster/logs/coll_box-%j.out

set -euo pipefail
source /clusteruy/home03/esys/luiz.gomes/miluphcuda/.cluster/env.sh
RUN="$MCU_ROOT/.cluster/runs/coll_box-$SLURM_JOB_ID"
mkdir -p "$MCU_ROOT/.cluster/runs"
mkdir "$RUN"
mkdir "$RUN/source" "$RUN/tmp"
export TMPDIR="$RUN/tmp"
cd "$RUN"
echo "Host=$(hostname) Job=$SLURM_JOB_ID Results=$RUN"

# Keep both main installations intact, including Luiz's original 3D binary.
sha256sum "$MCU_ROOT/build/miluphcuda" "$MCU_ROOT/include/parameter.h" \
  "$MCU_ROOT/Makefile" > main-before.sha256
if [[ $(id -un) == mauro.pico ]]; then
  sha256sum /clusteruy/home/mauro.pico/simulator/vendor/miluphcuda/build/miluphcuda \
    /clusteruy/home/mauro.pico/simulator/vendor/miluphcuda/include/parameter.h \
    /clusteruy/home/mauro.pico/simulator/vendor/miluphcuda/include/rk2adaptive.h \
    /clusteruy/home/mauro.pico/simulator/vendor/miluphcuda/Makefile >> main-before.sha256
fi
verify_main() {
  result=$?
  trap - EXIT
  sha256sum --check "$RUN/main-before.sha256" || result=1
  exit "$result"
}
trap verify_main EXIT

# Ordinary copies, no links to mutable source or build files.
cp -R "$MCU_ROOT/src" "$MCU_ROOT/include" "$RUN/source/"
cp "$MCU_ROOT/Makefile" "$RUN/source/Makefile"
cp "$MCU_ROOT/coll_box/parameter.h" "$RUN/source/include/parameter.h"
cp "$MCU_ROOT/coll_box/material.cfg" "$RUN/material.cfg"
cp "$MCU_ROOT/coll_box/basalt.till.cfg" "$RUN/basalt.till.cfg"
cp "$MCU_ROOT/coll_box/sand.till.cfg" "$RUN/sand.till.cfg"
cp "$MCU_ROOT/coll_box/simu.0000" "$RUN/simu.0000"
cp "$MCU_ROOT/coll_box/boundary.cu" "$RUN/source/src/boundary.cu"
#cp "$MCU_ROOT/test_cases/colliding_rings/generate_initial_rings.py" "$RUN/generate_initial_rings.upstream.py"

(
  cd source
  make -j "${SLURM_CPUS_PER_TASK:-1}" CUDA_DIR=/usr/local/cuda \
    GPU_ARCH=-arch=sm_86 \
    INCLUDE_DIRS="-Iinclude -I/usr/local/cuda/include -I$MCU_ROOT/.cluster/lib -I/usr/include" \
    LDFLAGS="-ccbin /usr/bin/g++ -L/usr/local/cuda/lib64 -L/usr/lib64 $MCU_ROOT/.cluster/lib/libconfig.a -lcudart -lpthread -lhdf5 -lm" \
    > "$RUN/build.log" 2>&1
)
echo 'Build OK; running sand: -n 5 -t 5 -H -d 0'
./source/build/miluphcuda -n 150 -t 0.02 -H -d 0 -f simu.0000 -m material.cfg > run.log 2>&1

# HDF5 C API avoids needing a separate Python scientific environment.
gcc -std=c99 -O2 "$MCU_ROOT/.cluster/check-sand.c" -o check-coll_box -lhdf5 -lm
./check-coll_box "$N" > verification.txt
cat verification.txt
touch SMOKE_OK
echo "SMOKE_OK: $RUN"
