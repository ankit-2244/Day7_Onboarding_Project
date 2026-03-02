"""
Developer Onboarding Script - Part B
Checks if developer environment is correctly set up, including advanced features.
"""

# -----------------------------
# Imports
# -----------------------------
from onboard import check_python_version, check_virtual_environment, check_internet
import argparse
import sys
import subprocess
import shutil
import time

# -----------------------------
# Command-line arguments
# -----------------------------
parser = argparse.ArgumentParser(description="Developer Onboarding Script")
parser.add_argument("--verbose", action="store_true", help="Show extra details")
parser.add_argument("--fix", action="store_true", help="Try to fix missing packages automatically")
args = parser.parse_args()

# -----------------------------
# Check if a package is installed
# -----------------------------
def check_package(pkg_name):
    try:
        module = __import__(pkg_name)
        msg = f"[PASS] {pkg_name} installed: version {module.__version__}"
    except ImportError:
        if args.fix:
            print(f"{pkg_name} missing, trying to install...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
            return check_package(pkg_name)  # re-check after installing
        else:
            msg = f"[FAIL] {pkg_name} not installed!"
    if args.verbose:
        print(msg)
    return msg

# -----------------------------
# Disk space check
# -----------------------------
def check_disk_space():
    total, used, free = shutil.disk_usage(".")
    free_gb = free / (1024 ** 3)
    if free_gb < 1:
        msg = f"[WARN] Low disk space: {free_gb:.2f} GB free"
    else:
        msg = f"[PASS] Disk space OK: {free_gb:.2f} GB free"
    if args.verbose:
        print(msg)
    return msg

# -----------------------------
# Run all checks and save report
# -----------------------------
def generate_report():
    start_time = time.time()
    results = []

    # List of all checks
    checks = [
        check_python_version,
        check_virtual_environment,
        lambda: check_package("numpy"),
        lambda: check_package("pylint"),
        lambda: check_package("black"),
        lambda: check_package("requests"),
        check_internet,
        check_disk_space
    ]

    for check in checks:
        t0 = time.time()
        result = check()

        # Convert tuples from Part A or bool results to string messages
        if isinstance(result, tuple):
            passed, info = result
            result = f"[PASS] {info}" if passed else f"[FAIL] {info}"
        elif isinstance(result, bool):
            result = "[PASS]" if result else "[FAIL]"

        t1 = time.time()
        if args.verbose:
            print(f"Check took {t1 - t0:.2f} seconds")
        results.append(result)

    total_time = time.time() - start_time

    # Save report
    with open("setup_report.txt", "w", encoding="utf-8") as f:
        f.write("=== Developer Onboarding Check ===\n")
        for line in results:
            f.write(line + "\n")
        passed = sum(1 for r in results if "[PASS]" in r)
        f.write(f"-- Result: {passed}/{len(results)} checks passed ✓\n")
        f.write(f"Total execution time: {total_time:.2f} seconds\n")

    # Print report
    print("\n".join(results))
    print(f"Report saved to setup_report.txt (Total time: {total_time:.2f}s)")

# -----------------------------
# Run the script
# -----------------------------
if __name__ == "__main__":
    generate_report()