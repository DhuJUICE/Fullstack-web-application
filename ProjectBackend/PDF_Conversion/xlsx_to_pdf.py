import os
import win32com.client

def xlsx_to_pdf(xlsx_path):
    # Get the directory and filename of the input file
    directory, filename = os.path.split(xlsx_path)
    
    # Change the extension to .pdf for the output file
    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
    pdf_path = os.path.join(directory, pdf_filename)
    
    # Initialize Excel application
    excel = win32com.client.Dispatch("Excel.Application")
    
    try:
        # Open the Excel workbook
        workbook = excel.Workbooks.Open(xlsx_path)
        
        # Save the workbook as PDF
        workbook.ExportAsFixedFormat(0, pdf_path)  # 0 is the FileFormat for PDF
        
        # Success message
        print(f"Successfully converted '{xlsx_path}' to '{pdf_path}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the workbook and quit Excel
        workbook.Close(False)
        excel.Quit()

# Path to the uploaded Excel file
xlsx_path = r"A:\Personal\Grocery List.xlsx"  

# Convert the uploaded Excel file to PDF
xlsx_to_pdf(xlsx_path)
