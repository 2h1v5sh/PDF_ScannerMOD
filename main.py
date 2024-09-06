import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import sys
import argparse
from modules import yara_handler, pdf_scanner, config_manager, log_manager

logger = log_manager.setup_logging()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan PDF files for potential threats using YARA rules.")
    parser.add_argument('paths', metavar='path', type=str, nargs='+', help='PDF files or directories to scan')
    parser.add_argument('-c', '--config', type=str, help='Path to configuration file', required=False)
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use', default=os.cpu_count())
    return parser.parse_args()

def get_pdf_files(paths):
    pdf_files = []
    for path in paths:
        if os.path.isfile(path) and path.lower().endswith('.pdf'):
            pdf_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        else:
            logger.warning(f"'{path}' is not a valid file or directory.")
    return pdf_files

def main():
    args = parse_arguments()
    config = config_manager.load_config(args.config)
    yara_rules = yara_handler.load_yara_rules(config['yara']['rules_path'])

    pdf_files = get_pdf_files(args.paths)
    if not pdf_files:
        logger.error("No PDF files found to scan.")
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_file = {executor.submit(pdf_scanner.scan_pdf, file, yara_rules): file for file in pdf_files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error scanning file {file}: {e}")

    logger.info("Scanning complete. Check logs for detailed results.")

if __name__ == "__main__":
    main()
