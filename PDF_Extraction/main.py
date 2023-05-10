import fitz  # install using: pip install PyMuPDF


# Function to extract text from PDF files
def text_from_pdf(path):
    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


# if the script is running from the main directory, execute the extract function
if __name__ == "__main__":
    print(text_from_pdf('Sample_Data/1.pdf'))