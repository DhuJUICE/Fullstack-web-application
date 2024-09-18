from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def create_license_pdf(license_text):
    # Create a PDF with the license text
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Add the license text at coordinates (100, 800)
    can.drawString(100, 800, license_text)
    can.save()
    
    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    return packet

def prepend_license_to_pdf(original_pdf_path, license_text, output_pdf_path):
    # Create a PDF with the license text
    license_pdf = create_license_pdf(license_text)
    
    # Read the original PDF
    original_pdf = PdfReader(original_pdf_path)
    
    # Create a new PDF writer
    output_pdf = PdfWriter()
    
    # Add the license page first
    license_reader = PdfReader(license_pdf)
    output_pdf.add_page(license_reader.pages[0])
    
    # Add all pages from the original PDF
    for page_num in range(len(original_pdf.pages)):
        output_pdf.add_page(original_pdf.pages[page_num])
    
    # Write the combined PDF to a file
    with open(output_pdf_path, 'wb') as output_file:
        output_pdf.write(output_file)

# Example usage
license_text = "This document is licensed under NexTech License."
original_pdf_path = "Rename.pdf"
output_pdf_path = "output_with_license.pdf"

prepend_license_to_pdf(original_pdf_path, license_text, output_pdf_path)
