import os
import win32com.client

def pptx_to_pdf(pptx_path):
    # Get the directory and filename of the input file
    directory, filename = os.path.split(pptx_path)
    
    # Change the extension to .pdf for the output file
    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
    pdf_path = os.path.join(directory, pdf_filename)
    
    # Initialize PowerPoint application
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    
    try:
        # Open the presentation
        presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
        
        # Save the presentation as PDF
        presentation.SaveAs(pdf_path, FileFormat=32)  # 32 is the FileFormat for PDF
        
        # Success message
        print(f"Successfully converted '{pptx_path}' to '{pdf_path}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the presentation and quit PowerPoint
        presentation.Close()
        powerpoint.Quit()

# Path to the uploaded PowerPoint file
pptx_path = r"A:\Personal\Transaction Management.pptx" 

# Convert the uploaded PowerPoint file to PDF
pptx_to_pdf(pptx_path)
