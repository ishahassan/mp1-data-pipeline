"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    import logging

def setup_logging(verbose=False):
    """
    Configure Python's logging system.

    -Use `logging.DEBUG` when `verbose` is `True`.
    -Use `logging.INFO` when `verbose` is `False`.
    -Include the **time, log level, and message** in each log entry.
    """

    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S"
    )

    return logging.getLogger(__name__)



def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")

    parser.add_argument("--input", 
                        "-i",
                        required=True, 
                        help="Path to the input data file")
    
    parser.add_argument("--output", 
                        "-o",
                        required=True, 
                        help="Path to the output data file")
    
    parser.add_argument("--format", 
                        choices=["csv", "json"], 
                        default="csv", 
                        help="Output format (default: csv)")
    
    parser.add_argument("--verbose", 
                        "-v",
                        action="store_true", 
                        help="Enable verbose logging")

    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file.
    Validate that the input path exists and is a file.

    Returns:
        True  — if the file exists
        False — if the file does not exist
    """

    logger = logging.getLogger(__name__)
    p = Path(filepath)

    if not p.is_file():
        logger.error(f"Input file not found: {filepath}")
        return False

    logger.info(f"Input file validated: {filepath}")
    return True


def main():
    """Main pipeline function."""
    # 1. Parse command-line arguments
    args = parse_arguments()

    # 2. Set up logging using the --verbose option
    logger = setup_logging(verbose=args.verbose)

    # 3. Log the parsed arguments at DEBUG level
    logger.debug(
        f"Arguments parsed: input={args.input}, output={args.output}, format={args.format}"
    )

    # 4. Validate the input file
    if not validate_input(args.input):
        # 5. Exit with status code 1 if invalid
        sys.exit(1)


if __name__ == "__main__":
    main()