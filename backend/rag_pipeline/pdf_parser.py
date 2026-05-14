import pdfplumber
import os


class PDFParser:
    def parse(self, file_path: str) -> list[str]:
        """
        Parse a PDF and return a list of page text strings.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF not found: {file_path}")

        pages = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text.strip())

        return pages  # list[str], one entry per page