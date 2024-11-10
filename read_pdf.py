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

def deep_ocr(image):
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    image = Image.open(image    ).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def group_pdfs_by_lecture(directory):
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

def pdf_to_images(pdf_path, dpi=300):
    try:
        return convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        Exception(f"Error converting PDF to images: {e}")

def preprocess_image(image):
    # Convert PIL Image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Noise removal with morphological operations
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return processed

def ocr_image(image):
    # Convert OpenCV image back to PIL format
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Configure Tesseract to treat the image as a single text line
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text

def ocr_pdf(pdf_path, output_folder='temp_images', dpi=300):
    images = pdf_to_images(pdf_path)
    processed_images = [preprocess_image(img) for img in images]  # pyright: ignore
    extracted_text = ""
    for idx, img in enumerate(processed_images):
        text = deep_ocr(img)
        extracted_text += text

    return extracted_text

def extract_text_from_pdf(pdf_path):
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

if __name__ == "__main__":
    # pdf_path = '/Users/dhrumeen/Downloads/685/4_notes.pdf'
    # print(ocr_pdf(pdf_path))
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
