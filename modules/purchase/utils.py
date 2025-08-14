import fitz 
import re
from dateutil import parser as dateparser
from typing import Optional, Dict

def extract_text_from_pdf(file_path: str) -> str:
    # return text from pdf
    doc = fitz.open(file_path)
    text_path = []
    for page in doc:
        text_path.append(page.get_text("text"))
    doc.close()
    return "\n".join(text_path)


def parse_po_details(text: str) -> Dict[str, Optional[str]]:
    txt = re.sub(r'\s+', ' ', text)
    #PO Number
    po_no_patterns = [
        r"PO No\s*[:\-]?\s*([A-Za-z0-9\-_]+)",
        r"PO\s*Number\s*[:\-]?\s*([A-Za-z0-9\-_]+)",
        r"\b(MH[0-9]{3,}|PO[0-9A-Za-z\-_]+)\b"  
    ]
    po_number = None
    for pat in po_no_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            po_number = m.group(1).strip()
            break

    #PO Date
    po_date = None
    date_patterns = [
        r"PO Date\s*[:\-]?\s*([A-Za-z0-9, \-\/]+)",
        r"PO Date\s*[:\-]?\s*([0-9]{1,2}\s*[A-Za-z]{3,}\s*[0-9]{4})",
        r"PO\s*Date\s*[:\-]?\s*([0-9/\-\.]{6,})"
    ]
    for pat in date_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            try:
                parsed = dateparser.parse(raw, dayfirst=False)
                po_date = parsed.date()
                break
            except Exception:
                pass

    #Total / Grand Total / Total Amount
    total_amount = None
    total_patterns = [
        r"Grand Total\s*\(INR\)\s*[:\-]?\s*([0-9,]+\.\d{2})",
        r"Grand Total\s*[:\-]?\s*([0-9,]+\.\d{2})",
        r"Total Amount\s*\(INR\)\s*[:\-]?\s*([0-9,]+\.\d{2})",
        r"Total Amount\s*[:\-]?\s*([0-9,]+\.\d{2})",
        r"Total\s*Amount\s*[:\-]?\s*([0-9,]+\.\d{2})",
        r"Total\s.*?([0-9,]+\.\d{2})"
    ]
    for pat in total_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            num = m.group(1).replace(',', '')
            try:
                total_amount = float(num)
                break
            except:
                pass

    return {
        "po_number": po_number,
        "po_date": po_date,
        "total_amount": total_amount
    }
