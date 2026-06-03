import os
import re
import time
import io
import requests
from pypdf import PdfReader, PdfWriter

# ΝΕΟΣ ΦΑΚΕΛΟΣ ΓΙΑ ΤΑ PDF
PDF_DIR = r"C:\Users\User\Desktop\EMY_DATA\pdf"
os.makedirs(PDF_DIR, exist_ok=True)

BASE_URL = "http://oldportal.emy.gr/emy/el/climatology/load_bulletin_html?fileid="

MONTH_MAP = {
    'JANUARY': 'JAN', 'JAN': 'JAN', 'FEBRUARY': 'FEB', 'FEB': 'FEB', 'MARCH': 'MAR', 'MAR': 'MAR',
    'APRIL': 'APR', 'APR': 'APR', 'MAY': 'MAY', 'JUNE': 'JUN', 'JUN': 'JUN', 'JULY': 'JUL', 'JUL': 'JUL',
    'AUGUST': 'AUG', 'AUG': 'AUG', 'SEPTEMBER': 'SEP', 'SEP': 'SEP', 'OCTOBER': 'OCT', 'OCT': 'OCT',
    'NOVEMBER': 'NOV', 'NOV': 'NOV', 'DECEMBER': 'DEC', 'DEC': 'DEC'
}
month_regex_pattern = re.compile("|".join(sorted(MONTH_MAP.keys(), key=len, reverse=True)))

print(f"🚀 Έναρξη Λήψης (ΜΟΝΟ 4η Σελίδα) στον φάκελο: {PDF_DIR} ...")

for file_id in range(244, 488):
    url = f"{BASE_URL}{file_id}"
    response = None
    
    for attempt in range(1, 4):
        try:
            time.sleep(1)
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                response = res
                break
            elif res.status_code == 500:
                break
        except:
            time.sleep(3)
            
    if not response or "application/pdf" not in response.headers.get("Content-Type", "") and not response.content.startswith(b"%PDF"):
        continue

    try:
        pdf_in = PdfReader(io.BytesIO(response.content))
        
        if len(pdf_in.pages) >= 4:
            target_page = pdf_in.pages[3]
        else:
            target_page = pdf_in.pages[-1] 

        raw_filename = ""
        cd = response.headers.get("Content-Disposition", "")
        match = re.search(r"filename=['\"]?([^\s'\"<>]+)", cd)
        if match:
            raw_filename = match.group(1).replace(".pdf", "").upper()
            
        final_month = "JAN" if file_id == 244 else None
        final_year = "2016" if file_id == 244 else None
        
        if file_id != 244:
            m_match = month_regex_pattern.search(raw_filename)
            if m_match: final_month = MONTH_MAP[m_match.group(0)]
            y_matches = re.findall(r"20[1-2]\d", raw_filename)
            if y_matches: final_year = y_matches[-1]

        clean_filename = f"{final_month}_{final_year}.pdf" if (final_month and final_year) else f"UNKNOWN_ID_{file_id}.pdf"
        
        pdf_out = PdfWriter()
        pdf_out.add_page(target_page)
        
        # Αποθήκευση στον υποφάκελο pdf
        full_path = os.path.join(PDF_DIR, clean_filename)
        with open(full_path, "wb") as f:
            pdf_out.write(f)
            
        print(f"✅ ID {file_id} -> Αποθηκεύτηκε η Σελίδα 4 ως: {clean_filename}")
        
    except Exception as e:
        print(f"❌ Σφάλμα επεξεργασίας PDF στο ID {file_id}: {e}")