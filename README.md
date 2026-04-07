# ChampSim Cache Replacement and Prefetching Study

This project investigates the impact of different L2 cache replacement policies and prefetching techniques on cache performance using the ChampSim simulator.

## Overview

We compare three configurations:
- **LRU** (Least Recently Used) replacement with **no prefetcher**
- **SHiP** (Signature-based Hit Predictor) replacement with **no prefetcher**
- **SHiP** replacement with **SPP** (Signature Path Prefetcher)

Each configuration is evaluated with five L2 cache sizes (128 KB, 256 KB, 512 KB (2x), 1024 KB) by varying sets and ways.

## Benchmarks (Traces)

Three memory-intensive SPEC CPU traces are used (choose any three from the [ChampSim trace repository](https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/)). Recommended:
- `625.x264_s-39B.champsimtrace.xz` (video encoding)
- `456.hmmer-327B.champsimtrace.xz` (database search)
- `437.leslie3d-273B.champsimtrace.xz` (hydrodynamics)

## Cache Configurations

Cache line size: 64 bytes. Cache size = `sets × ways × 64`.

| sets | ways | size (KB) |
|------|------|-----------|
| 256  | 8    | 128       |
| 512  | 8    | 256       |
| 512  | 16   | 512       |
| 1024 | 8    | 512       |
| 1024 | 16   | 1024      |

## Build requirements

- Kali Linux 2026.1
- CMake (≥3.20, recommend 3.28)
- g++ (≥9), make, ninja-build
- Python 3 with `jinja2` module
- Git
- Simulator ChampSim

## Installation

Clone ChampSim with submodules:
```bash
git clone --recursive https://github.com/ChampSim/ChampSim.git
cd ChampSim
```

Set up vcpkg dependencies:
```bash
./vcpkg/bootstrap-vcpkg.sh
./vcpkg/vcpkg install
```

If you encounter CMake version issues (≥3.30), use CMake 3.28:
```bash
wget https://github.com/Kitware/CMake/releases/download/v3.28.3/cmake-3.28.3-linux-x86_64.tar.gz
tar -xzf cmake-3.28.3-linux-x86_64.tar.gz
sudo mv cmake-3.28.3-linux-x86_64 /opt/cmake-3.28.3
export PATH=/opt/cmake-3.28.3/bin:$PATH
```



## Downloading Traces

Inside `ChampSim/`:
```bash
wget https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/625.x264_s-39B.champsimtrace.xz
wget https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/456.hmmer-327B.champsimtrace.xz
wget https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/437.leslie3d-273B.champsimtrace.xz
```

Create a `traces/` directory and move the traces there.

## Building All Binaries Automatically
For compile configurations, you need to run
```bash
python3 research_different_configs.py
```
Or
```bash
make configurate
```

## Running Simulations in Parallel

For executing simulator in parallel with all tracers:
```bash
python3 parallel_execute.py
```
Or
```bash
make execution
```


## Extracting L2 Hit Rates
For extracting L2 hit rates to csv table:
```bash
python3 parse_logs.py
```
Or
```bash
make parsing
```

## Plotting Results
For getting graphic with result:
```bash
python3 get_graphics.py
```
Or
```bash
make get_info
```

## All process
If you want just get final result, just execute:
```bash
make clean
make
make run
```



## References

- ChampSim: https://github.com/ChampSim/ChampSim
- Traces: https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/
- SHiP paper: Wu et al., “SHiP: Signature-based Hit Predictor for High Performance Caching” (HPCA 2011)
- SPP paper: Kim et al., “Signature Path Prefetcher” (MICRO 2015)

