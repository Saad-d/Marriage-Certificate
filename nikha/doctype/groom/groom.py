from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import pytesseract
from PIL import Image
import io
import re
import pdf2image  # For PDF support
from frappe.utils import get_bench_path
import os

class Groom(Document):
    pass

@frappe.whitelist()
def scan_groom_id(file_url):
    """Process uploaded ID (image/PDF) and auto-fill Groom fields"""
    try:
        file = frappe.get_doc("File", {"file_url": file_url})
        file_content = file.get_content()

        # Check if file is PDF
        if file.file_name.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
        else:
            text = extract_text_from_image(file_content)

        if not text:
            return {"error": "No text could be extracted from the document"}

        groom_data = {
            "name": extract_field(text, r"(Name|Full Name)[:\s]+([A-Za-z ]+)", group=2),
            "age": extract_field(text, r"(Age|DOB)[:\s]+(\d+)", group=2),
            "father_name": extract_field(text, r"(Father|Father's Name)[:\s]+([A-Za-z ]+)", group=2)
        }

        # Validate extracted data
        if not groom_data.get("name"):
            return {"error": "Could not extract name. Please upload a clearer document."}

        return groom_data

    except Exception as e:
        frappe.log_error(f"Groom ID Scan Error: {str(e)}", "scan_groom_id")
        return {"error": f"Processing failed: {str(e)}"}

def extract_text_from_image(image_content):
    """Extract text from image using OCR"""
    try:
        img = Image.open(io.BytesIO(image_content))
        img = preprocess_image(img)  # Improve OCR accuracy
        return pytesseract.image_to_string(img)
    except Exception as e:
        frappe.log_error(f"Image OCR failed: {str(e)}")
        return None

def extract_text_from_pdf(pdf_content):
    """Convert PDF pages to images and extract text"""
    try:
        images = pdf2image.convert_from_bytes(pdf_content)
        full_text = ""
        for image in images:
            processed_img = preprocess_image(image)
            full_text += pytesseract.image_to_string(processed_img) + "\n"
        return full_text
    except Exception as e:
        frappe.log_error(f"PDF processing failed: {str(e)}")
        return None

def preprocess_image(img):
    """Improve image quality for OCR"""
    try:
        # Convert to grayscale
        img = img.convert('L')
        # Increase contrast
        img = img.point(lambda x: 0 if x < 140 else 255)
        return img
    except Exception as e:
        frappe.log_error(f"Image preprocessing failed: {str(e)}")
        return img  # Return original if processing fails

def extract_field(text, pattern, group=1):
    """Helper: Extract text using regex"""
    try:
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(group).strip() if match else None
    except:
        return None