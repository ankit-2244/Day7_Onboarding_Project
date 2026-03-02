"""
Developer Onboarding Script
Checks if developer environment is correctly set up.
"""

import sys
import subprocess
import importlib
import requests


def check_python_version():
    """Check if Python version is >= 3.10"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"{version.major}.{version.minor}"
    return False, f"{version.major}.{version.minor}"


def check_virtual_environment():
    """Check if running inside virtual environment"""
    return sys.prefix != sys.base_prefix


def check_package(package_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def check_internet():
    """Check internet connectivity"""
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False


def main():
    """Main function"""
    print("=== Developer Onboarding Check ===")

    pass_count = 0
    total_checks = 6
    report = []

    # Python version
    python_ok, version = check_python_version()
    if python_ok:
        print(f"[PASS] Python version: {version}")
        pass_count += 1
        report.append("Python version: PASS")
    else:
        print(f"[FAIL] Python version: {version}")
        report.append("Python version: FAIL")

    # Virtual environment
    if check_virtual_environment():
        print("[PASS] Virtual environment active")
        pass_count += 1
        report.append("Virtual environment: PASS")
    else:
        print("[FAIL] Virtual environment NOT active")
        report.append("Virtual environment: FAIL")

    # pylint
    if check_package("pylint"):
        print("[PASS] pylint installed")
        pass_count += 1
        report.append("pylint: PASS")
    else:
        print("[FAIL] pylint not installed")
        report.append("pylint: FAIL")

    # black
    if check_package("black"):
        print("[PASS] black installed")
        pass_count += 1
        report.append("black: PASS")
    else:
        print("[FAIL] black not installed")
        report.append("black: FAIL")

    # numpy
    if check_package("numpy"):
        print("[PASS] numpy installed")
        pass_count += 1
        report.append("numpy: PASS")
    else:
        print("[FAIL] numpy not installed")
        report.append("numpy: FAIL")

    # Internet
    if check_internet():
        print("[PASS] Internet connectivity OK")
        pass_count += 1
        report.append("Internet: PASS")
    else:
        print("[FAIL] No internet connectivity")
        report.append("Internet: FAIL")

    print(f"\nResult: {pass_count}/{total_checks} checks passed")

    # Save report to file
    with open("setup_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("Report saved to setup_report.txt")


if __name__ == "__main__":
    main()
