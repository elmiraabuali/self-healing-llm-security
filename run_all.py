import os
import subprocess
import sys
from pathlib import Path


EXPERIMENTS = [
    ("baseline", "0", "0"),
    ("input_only", "1", "0"),
    ("output_only", "0", "1"),
    ("combined", "1", "1"),
]


for name, input_on, output_on in EXPERIMENTS:

    print("\n================================")
    print("Running:", name)
    print("Input mitigation:", input_on)
    print("Output mitigation:", output_on)
    print("================================\n")

    # Copy current environment
    env = os.environ.copy()

    # Set switches for this experiment
    env["INPUT_MITIGATION"] = input_on
    env["OUTPUT_MITIGATION"] = output_on

    # Make a separate result folder
    result_dir = Path("results") / name
    result_dir.mkdir(parents=True, exist_ok=True)

    report_prefix = str((result_dir / name).resolve())

    command = [
        sys.executable,
        "-m",
        "garak",

        "--target_type",
        "function",

        "--target_name",
        "pipeline#generate",

        # One response for each attack prompt
        "--generations",
        "1",

        # Save report for this condition
        "--report_prefix",
        report_prefix,

        # Same two probes for every condition
        "--probes",
        "dan.DanInTheWild,promptinject.HijackLongPrompt",
    ]

    result = subprocess.run(command, env=env)

    if result.returncode != 0:
        print("\nExperiment stopped or failed:", name)
        sys.exit(1)


print("\n================================")
print("ALL FOUR EXPERIMENTS FINISHED")
print("================================")