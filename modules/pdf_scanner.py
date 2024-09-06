import fitz  # PyMuPDF
import os
import logging

logger = logging.getLogger(__name__)

def print_matches(file_path, matches):
    if matches:
        logger.warning(f"{file_path} is potentially malicious.")
        for match in matches:
            logger.warning(f"Detected rule: {match.rule}")
    else:
        logger.info(f"{file_path} is clean.")

def scan_pdf(file_path, rules):
    if not os.path.isfile(file_path):
        logger.error(f"The file '{file_path}' does not exist.")
        return

    try:
        pdf_document = fitz.open(file_path)
        pdf_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()
        matches = rules.match(data=pdf_text)
        print_matches(file_path, matches)
    except fitz.FileDataError:
        logger.warning(f"The file '{file_path}' is corrupted. Attempting to read raw data.")
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                matches = rules.match(data=file_data)
                print_matches(file_path, matches)
        except Exception as e:
            logger.error(f"Failed to read the corrupted file. Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing '{file_path}'. Error: {e}")
