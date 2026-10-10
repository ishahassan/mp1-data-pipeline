*Data Processing Pipeline*

This project implements a modular data‑cleaning pipeline that loads raw input data, validates required fields, applies configurable cleaning steps, and saves a cleaned output dataset. Data flows through the system in clearly defined stages: input validation, file loading, DataFrame validation, duplicate removal, missing‑value handling, outlier filtering, and final output generation. Each module in the src/ directory has a single responsibility: utils handles logging setup, input validation, and saving output; data_loaders loads CSV, JSON, and YAML files; data_validator checks required columns and numeric fields; data_processor applies cleaning operations based on the YAML configuration; and data_output logs saved results. The pipeline is orchestrated by pipeline.py, which coordinates all modules and reports the final cleaning summary. Configuration is fully externalized in a YAML file, allowing flexible control over validation rules and processing steps. The final output includes both a cleaned CSV file and a printed cleaning report summarizing rows and columns removed.


*Example Command*

Run the pipeline using the provided sample data:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
Expected Output: 
    INFO     src.utils        — Input file validated: fixtures/sample_data.csv
    INFO     src.utils        — Input file validated: config/config.yaml
    INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
    INFO     src.data_loaders — Loaded YAML file: config/config.yaml
    WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
    DEBUG    src.data_validator — Validation: 100 -> 98 rows
    INFO     __main__         — Validation complete: 100 -> 98 rows
    DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
    DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
    DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
    INFO     __main__         — Processing complete: 98 -> 92 rows
    DEBUG    src.data_output  — Saved 92 rows to output/clean.csv
    INFO     __main__         — Saved cleaned data to output/clean.csv
