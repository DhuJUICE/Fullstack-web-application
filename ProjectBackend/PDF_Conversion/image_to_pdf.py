import os
from PIL import Image

def image_to_pdf(image_path):
    # Get the directory and filename of the input file
    directory, filename = os.path.split(image_path)
    
    # Change the extension to .pdf for the output file
    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
    pdf_path = os.path.join(directory, pdf_filename)
    
    try:
        # Open the image file
        image = Image.open(image_path)
        
        # Convert the image to RGB mode (PDFs don't support transparency)
        if image.mode in ("RGBA", "LA"):
            image = image.convert("RGB")
        
        # Save the image as a PDF
        image.save(pdf_path, "PDF", resolution=100.0)
        
        # Success message
        print(f"Successfully converted '{image_path}' to '{pdf_path}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the uploaded image file
image_path = r"A:\Personal\goku.jpg"  

# Convert the uploaded image file to PDF
image_to_pdf(image_path)
