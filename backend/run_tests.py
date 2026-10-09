#!/usr/bin/env python3
"""
Test runner script for the File Comparison Backend
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"Command failed with exit code: {result.returncode}")
        return False
    
    return True


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Test runner for File Comparison Backend")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--api", action="store_true", help="Run API tests only")
    parser.add_argument("--logging", action="store_true", help="Run logging tests only")
    parser.add_argument("--processor", action="store_true", help="Run processor tests only")
    parser.add_argument("--comparison", action="store_true", help="Run comparison tests only")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fast", action="store_true", help="Run fast tests only (skip slow)")
    
    args = parser.parse_args()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    import os
    os.chdir(backend_dir)
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add coverage
    if args.coverage:
        cmd.extend([
            "--cov=backend",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
    
    # Determine which tests to run
    test_paths = []
    markers = []
    
    if args.unit:
        markers.append("unit")
    elif args.integration:
        markers.append("integration")
    elif args.api:
        markers.append("api")
    elif args.logging:
        markers.append("logging")
    elif args.processor:
        markers.append("processor")
    elif args.comparison:
        markers.append("comparison")
    else:
        # Default: run all tests
        test_paths.append("tests/")
    
    # Skip slow tests if --fast is specified
    if args.fast:
        markers.append("not slow")
    
    # Add markers to command
    if markers:
        cmd.extend(["-m", " and ".join(markers)])
    
    # Add test paths
    cmd.extend(test_paths)
    
    # Add additional options
    cmd.extend([
        "--tb=short",
        "--strict-markers"
    ])
    
    # Run the tests
    success = run_command(cmd, f"Running tests: {' '.join(markers) if markers else 'all'}")
    
    if success and args.coverage:
        print("\nCoverage report generated in 'htmlcov/' directory")
        print("Open 'htmlcov/index.html' to view the report")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()