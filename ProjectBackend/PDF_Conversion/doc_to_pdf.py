import os
import win32com.client

def docx_to_pdf(docx_path):
    # Get the directory and filename of the input file
    directory, filename = os.path.split(docx_path)
    
    # Change the extension to .pdf for the output file
    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
    pdf_path = os.path.join(directory, pdf_filename)
    
    # Initialize Word application
    word = win32com.client.Dispatch("Word.Application")
    
    try:
        # Open the Word document
        doc = word.Documents.Open(docx_path)
        
        # Save the document as PDF
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 is the FileFormat for PDF
        
        # Success message
        print(f"Successfully converted '{docx_path}' to '{pdf_path}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the document and quit Word
        doc.Close(False)
        word.Quit()

# Path to the uploaded Word file
docx_path = r"A:\Personal\Hello World.docx"

# Convert the uploaded Word file to PDF
docx_to_pdf(docx_path)
