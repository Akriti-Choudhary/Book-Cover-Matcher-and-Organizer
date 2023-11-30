import os
import fitz
from PIL import Image
import imagehash
import shutil

def compute_phash(image_path):
    img = Image.open(image_path).convert("L")
    return imagehash.phash(img)

def find_first_cover_image(pdf_directory, output_image):
    first_pdf_file = os.path.join(pdf_directory, "first_book.pdf")

    pdf_document = fitz.open(first_pdf_file)
    first_page = pdf_document.load_page(0)
    pix = first_page.get_pixmap()
    pix.save(output_image)
    pdf_document.close()

    return compute_phash(output_image)

# Path to the directory containing the subdirectories with PDF files
main_directory = "C:/Users/KIIT/OneDrive/Desktop/Test/Books"
first_cover_image = "cover1.png"
pdf_file1 = "Git_Book.pdf"

pdf_document1 = fitz.open(pdf_file1)
first_page1 = pdf_document1.load_page(0)
pix1 = first_page1.get_pixmap()
pix1.save(first_cover_image)
pdf_document1.close()

phash1 = compute_phash(first_cover_image)

# Flag to check if the first cover does not match with any other cover
first_cover_matched = False

# Iterate through subdirectories
for subdir, _, files in os.walk(main_directory):
    for pdf_file in files:
        if pdf_file.endswith(".pdf"):
            full_pdf_path = os.path.join(subdir, pdf_file)

            # Compute pHash for the cover image of the current PDF
            output_image = "cover2.png"  # Overwrite the same cover image for every book
            pdf_document = fitz.open(full_pdf_path)
            first_page = pdf_document.load_page(0)
            pix = first_page.get_pixmap()
            pix.save(output_image)
            pdf_document.close()

            phash2 = compute_phash(output_image)

            # Compare the pHash values
            if not first_cover_matched:
                if phash1 - phash2 == 0:
                    # print(f"Cover images of '{pdf_file}' match with the first cover.")
                    first_cover_matched = True
                    break
                # else:
                #     print(f"Cover images of '{pdf_file}' do not match with the first cover.")

# If the first cover did not match with any other covers, copy the first book to the main directory
#print("first_cover_matched: ",first_cover_matched)
if not first_cover_matched:
    first_pdf_file = os.path.join("C:/Users/KIIT/OneDrive/Desktop/Test", "Git_Book.pdf")
    destination_path = os.path.join("C:/Users/KIIT/OneDrive/Desktop/Test/Books", "Git_Book.pdf")
    try:
        shutil.copy(first_pdf_file, destination_path)
        print("File copied successfully.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")
else:
    print("The book is already here.")

