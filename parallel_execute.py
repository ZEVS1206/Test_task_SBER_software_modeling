#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
import glob

#base paths
Base_dir = Path(__file__).parent.resolve()
ChampSim_dir = Base_dir / "ChampSim"

tracers_dir = ChampSim_dir / "tracers"
bin_dir     = ChampSim_dir / "bin"
results_dir = Path("./results")
warmup      = 50000000
simulation  = 100000000
max_parallel = cpu_count() - 1

def run_one_process(args):
    binary_file, trace, warmup, simulation = args
    trace_name = Path(trace).stem
    binary_file_name = Path(binary_file).name
    log_file = results_dir / f"{binary_file_name}_{trace_name}.log"
    cmd = [
        binary_file,
        f"--warmup-instructions={warmup}",
        f"--simulation-instructions={simulation}",
        trace
    ]
    with open(log_file, "w") as file:
        result = subprocess.run(cmd, stdout = file, stderr = subprocess.STDOUT)
    return (binary_file, trace, result.returncode, log_file)

def main():
    Path(results_dir).mkdir(exist_ok = True)

    binaries = glob.glob(f"{bin_dir}/champsim_*")
    if (not binaries):
        print(f"No binaries found in {bin_dir}")
        return

    tracers = glob.glob(f"{tracers_dir}/*.xz")
    if (not tracers):
        print(f"No tracers found in {tracers_dir}")
        return

    tasks = []
    for bin in binaries:
        for trace in tracers:
            tasks.append((bin, trace, warmup, simulation))

    print(f"Total tasks: {len(tasks)}")
    print(f"Running up to {max_parallel} parallel processes...")

    with Pool(processes = max_parallel) as pool:
        results = pool.map(run_one_process, tasks)
    failed = [r for r in results if r[2] != 0]
    if failed:
        print(f"Failed {len(failed)} tasks:")
        for f in failed:
            print(f"  {f[0]} on {f[1]}")
    else:
        print("All tasks completed successfully.")

if __name__ == "__main__":
    main()

