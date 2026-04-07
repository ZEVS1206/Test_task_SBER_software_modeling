#!/usr/bin/env python3

import json
import subprocess
import shutil
import os
import sys
from pathlib import Path

#base paths
Base_dir = Path(__file__).parent.resolve()
ChampSim_dir = Base_dir / "ChampSim"

#configuration files
Template_config = ChampSim_dir / "champsim_config.json"
Work_config     = ChampSim_dir / "champsim_work_config.json"

#Array of configurations
Configurations = [("lru", "no"), ("ship", "no"), ("ship", "spp_dev")]

#Array of (set, way)
Params = [(256, 8),    #128 kB
          (512, 8),    #256 kB
          (512, 16),   #512 kB
          (1024, 8),   #512 kB
          (1024, 16)]  #1024 kB

def build_binary(replacement, prefetching, sets, ways):
    print(f"Build configuration with:\n\treplacement={replacement}\n\tprefetching={prefetching}\n\tsets={sets}\n\tways={ways}")
    with open(Template_config, "r") as tmp_file:
        config = json.load(tmp_file)
    #Change L2 parametres
    config["L2C"]["replacement"] = replacement
    config["L2C"]["prefetcher"]  = prefetching
    config["L2C"]["sets"]        = sets
    config["L2C"]["ways"]        = ways
    with open(Work_config, "w") as tmp_file:
        json.dump(config, tmp_file, indent=2)

    #Execute config.sh
    subprocess.run(["./config.sh", Work_config], check=True, cwd=ChampSim_dir)

    #Execute make
    subprocess.run(["make", "-j", str(os.cpu_count())], check=True, cwd=ChampSim_dir)

    #Copy binary file in folder bin/
    bin_name = f"champsim_{replacement}_{prefetching}_{sets}_{ways}"
    source_bin = ChampSim_dir / "bin" / "champsim"
    dest_bin   = ChampSim_dir / "bin" / bin_name
    shutil.copy(source_bin, dest_bin)
    print(f"Created {bin_name}")

    #Clean configuration files for the next build
    subprocess.run(["./clean.sh", ""], check=True)

def main():
    if not Template_config.exists():
        print(f"Error: {Template_config} not found")
        sys.exit(1)

    (ChampSim_dir / "bin").mkdir(exist_ok=True)
    for repl, pref in Configurations:
        for sets, ways in Params:
            try:
                build_binary(repl, pref, sets, ways)
            except subprocess.CalledProcessError as e:
                print(f"Failed at {repl}/{pref}/{sets}/{ways}: {e}")
                sys.exit(1)
    print("All binaries built successfully.")

if __name__ == "__main__":
    main()
