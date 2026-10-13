"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
from logging import config
import sys
# from data_processor import process_data, create_cleaning_report
from pathlib import Path
# from data_loaders import load_data

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


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


def main():
    """Main pipeline function."""
    # 1. Parse command-line arguments
    args = parse_arguments()

    # 2. Set up logging using the --verbose option
    setup_logging(verbose=args.verbose)

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

        required_columns = config["validation"]["required_columns"]
        numeric_columns = config["validation"]["numeric_columns"]


    except ValueError as e:
        logger.error(f"Failed to load data: {e}")
        sys.exit(1)

    df_before = data.copy()

    # - Before processing, call `validate_dataframe()` inside a separate `try`/`except` block. Catch `ValueError` and exit with status code `1`. 
    try:
        df_validated = validate_dataframe(df_before, required_columns, numeric_columns)
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    logger.info(f"Validation complete: {len(df_before)} -> {len(df_validated)} rows")

    df_before = df_validated.copy()
    
    try:
        df_after = process_data(df_validated, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    logger.info(f"Processing complete: {len(df_validated)} -> {len(df_after)} rows")
    ### 6. Create the Output

    output_path = Path(args.output)
    save_data(df_after, output_path)
    logger.info(f"Saved cleaned data to {output_path}")

    report = create_cleaning_report(df_before, df_after)

    print("Cleaning Report:")
    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()