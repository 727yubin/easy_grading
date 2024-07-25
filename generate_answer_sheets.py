import pandas as pd
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import argparse
import os

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,  # Smaller box size for a smaller QR code
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def generate_printable_document(csv_file, num_pages):
    # Register a font that supports both English and Korean characters
    pdfmetrics.registerFont(TTFont('NotoSansKR', 'font.ttf'))
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Create a PDF document
    output = io.BytesIO()
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    
    for index, row in df.iterrows():
        student_id = row['ID']
        student_name = row['Name']
        for page_number in range(1, num_pages + 1):
            # Generate QR code
            qr_data = f"{student_id}_{page_number}"
            qr_img = generate_qr_code(qr_data)
            
            # Save QR code image to temporary file
            qr_img_path = f"/tmp/{student_id}_{page_number}.png"
            qr_img.save(qr_img_path)
            
            # Draw QR code on PDF with a box around it
            qr_x = width - 30*mm
            qr_y = height - 50*mm
            qr_size = 20 * mm
            c.drawImage(qr_img_path, qr_x, qr_y, width=qr_size, height=qr_size)
            c.rect(qr_x, qr_y, qr_size, qr_size)  # Box around the QR code
            
            # Center the "DO NOT TAMPER WITH QR" text above the QR code
            c.setFont("Helvetica", 8)
            tamper_text = "DO NOT TAMPER WITH QR"
            text_width = c.stringWidth(tamper_text, "Helvetica", 8)
            c.drawString(qr_x + (qr_size - text_width) / 2, qr_y - 10, tamper_text)
            
            # Add header text (name, ID, page number) in bold
            header_text = f"Name: {student_name}    ID: {student_id}    Page: {page_number}/{num_pages}"
            c.setFont("NotoSansKR", 12)
            x = 10 * mm
            y = height - 20 * mm
            for dx, dy in [(0, 0), (0.2, 0), (0, 0.2), (0.2, 0.2)]:
                c.drawString(x + dx, y + dy, header_text)
            
            # Add a new page if not the last page
            if not (index == len(df) - 1 and page_number == num_pages):
                c.showPage()
    
    c.save()
    output.seek(0)
    
    # Save the PDF to a file
    pdf_filename = f"{os.path.splitext(csv_file)[0]}_printable_document.pdf"
    with open(pdf_filename, "wb") as f:
        f.write(output.read())
    print(f"PDF saved as {pdf_filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate printable documents with QR codes.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing student information.')
    parser.add_argument('num_pages', type=int, help='Number of pages per student.')
    
    args = parser.parse_args()
    
    generate_printable_document(args.csv_file, args.num_pages)

if __name__ == "__main__":
    main()
