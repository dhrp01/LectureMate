import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import cv2
import numpy as np

import os
import re
from collections import defaultdict
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

def group_pdfs_by_lecture(directory: str) -> dict:
    """
    Groups PDF files by lecture number based on their filenames.

    Args:
        directory (str): Path to the directory containing PDF files.

    Returns:
        dict: A dictionary where keys are lecture numbers and values are lists of file paths.
    """
    lecture_groups = defaultdict(list)
    pdf_pattern = re.compile(r'^(\d+)_.*\.pdf$', re.IGNORECASE)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            match = pdf_pattern.match(filename)
            if match:
                lecture_num = match.group(1)
                lecture_groups[lecture_num].append(os.path.join(directory, filename))
            else:
                print(f"Filename '{filename}' does not match the expected pattern and will be skipped.")

    return lecture_groups

def extract_text_from_pdf(pdf_path: str) -> str | None:
    """Extract text from the given pdf file

    Args:
        pdf_path: Path to the PDF file

    Returns:
        str of the extracted PDF
    """
    try:
        # Open the PDF file in binary mode
        with open(pdf_path, 'rb') as file:
            # Initialize the PDF reader
            reader = PyPDF2.PdfReader(file)
            text = ""

            # Iterate through each page and extract text
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"

        return text

    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def process_pdf(file) -> None:
    """Generate txt file using the given PDF file path content

    Args:
        path: Directory path containing all the PDF files
    """
    extracted_text = ""
    with open(f'train_text_data/50.txt', 'w+') as train_text:
        if 'notes' not in file:
            text = extract_text_from_pdf(file)
            extracted_text += f"\n{text}"
        train_text.write(extracted_text)

if __name__ == "__main__":
    pdf_path = '~/685/'  # Replace with your PDF file path
    grouped_pdfs = group_pdfs_by_lecture(pdf_path)
    print(len(grouped_pdfs))
    for lecture, files in grouped_pdfs.items():
            extracted_text = ""
            print(f"Lecture {lecture}:")
            with open(f'train_text_data/{int(lecture)+23}.txt', 'w+') as train_text:
                for file in files:
                    print(f"  - {file}")
                    if 'notes' in file:
                        continue
                    text = extract_text_from_pdf(file)
                    extracted_text += f"\n{text}"
                train_text.write(extracted_text)
