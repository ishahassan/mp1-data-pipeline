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
from data_processor import process_data, create_cleaning_report
from pathlib import Path
from data_loaders import load_data


logger = logging.getLogger(__name__)

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
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
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
    
    parser.add_argument("--config",
                    required=True,
                    help="Path to the YAML configuration file")
    
    parser.add_argument("--output", 
                        "-o",
                        required=True, 
                        help="Path to the output data file")

    
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
    f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}"
)

    # 4. Validate the input file
    if not validate_input(args.input):
        # 5. Exit with status code 1 if invalid
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    # Part 2: Load the file
    input_path = Path(args.input)
    config_path = Path(args.config)

    try:
        data = load_data(input_path)
        config = load_data(config_path)
    except ValueError as e:
        logger.error(f"Failed to load data: {e}")
        sys.exit(1)

    logger.info(f"Loaded data from {input_path}")

    df_before = data.copy()

    try:
        df_after = process_data(data, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    ### 6. Create the Output
    report = create_cleaning_report(df_before, df_after)

    print("Cleaning Report:")
    for key, value in report.items():
        print(f"{key}: {value}")


    logger.info(f"Processing complete: {len(df_before)} → {len(df_after)} rows")

    output_path = Path(args.output)
    df_after.to_csv(output_path, index=False)

    logger.info(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    main()