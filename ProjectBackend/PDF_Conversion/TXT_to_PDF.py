import os
from fpdf import FPDF

def txt_to_pdf(txt_file, pdf_file):
    # Create an instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set font for the PDF
    pdf.set_font("Arial", size=12)
    
    # Open the .txt file and read its content
    try:
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
                pdf.multi_cell(0, 10, line.strip())
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
    
    # Output the PDF to a file
    try:
        pdf.output(pdf_file)
        print(f"Successfully created {pdf_file}")
    except Exception as e:
        print(f"Error creating the PDF: {e}")

if __name__ == "__main__":
    # Example usage
    input_txt = "test.txt"
    output_pdf = "test.pdf"    
    if os.path.exists(input_txt):
        txt_to_pdf(input_txt, output_pdf)
    else:
        print("The specified .txt file does not exist.")
