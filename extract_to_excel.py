import os
import re
import pdfplumber
import pandas as pd

# ΟΡΙΣΜΟΣ ΦΑΚΕΛΩΝ
BASE_DIR = r"C:\Users\User\Desktop\EMY_DATA"
PDF_DIR = os.path.join(BASE_DIR, "pdf")

GREEK_MONTHS_MAP = {
    'ΙΑΝΟΥΑΡΙΟΣ': 1, 'ΦΕΒΡΟΥΑΡΙΟΣ': 2, 'ΜΑΡΤΙΟΣ': 3, 'ΑΠΡΙΛΙΟΣ': 4,
    'ΜΑΙΟΣ': 5, 'ΜΑΪΟΣ': 5, 'ΙΟΥΝΙΟΣ': 6, 'ΙΟΥΛΙΟΣ': 7, 'ΑΥΓΟΥΣΤΟΣ': 8,
    'ΣΕΠΤΕΜΒΡΙΟΣ': 9, 'ΟΚΤΩΒΡΙΟΣ': 10, 'ΝΟΕΜΒΡΙΟΣ': 11, 'ΔΕΚΕΜΒΡΙΟΣ': 12
}
inv_map = {v: k for k, v in zip(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'], range(1,13))}

all_data_rows = []

print(f"🚀 Έναρξη Έξυπνης Εξαγωγής από τα PDF του φακέλου: {PDF_DIR} ...")

# Διαβάζουμε πλέον από τον υποφάκελο PDF_DIR
pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

for filename in sorted(pdf_files):
    filepath = os.path.join(PDF_DIR, filename)
    file_match = re.match(r"([A-Z]{3})_(\d{4})", filename)
    month_en, year_out = file_match.groups() if file_match else ("UNKNOWN", "UNKNOWN")
        
    try:
        with pdfplumber.open(filepath) as pdf:
            page = pdf.pages[0]
            page_text = page.extract_text()
            
            if not page_text:
                continue
            
            if year_out == "UNKNOWN":
                compressed_text = page_text.upper().replace(" ", "").replace("\n", "")
                match = re.search(r'(ΙΑΝΟΥΑΡΙΟΣ|ΦΕΒΡΟΥΑΡΙΟΣ|ΜΑΡΤΙΟΣ|ΑΠΡΙΛΙΟΣ|ΜΑΙΟΣ|ΜΑΪΟΣ|ΙΟΥΝΙΟΣ|ΙΟΥΛΙΟΣ|ΑΥΓΟΥΣΤΟΣ|ΣΕΠΤΕΜΒΡΙΟΣ|ΟΚΤΩΒΡΙΟΣ|ΝΟΕΜΒΡΙΟΣ|ΔΕΚΕΜΒΡΙΟΣ).*?(20[1-2]\d)', compressed_text)
                if match:
                    gr_month = match.group(1).replace('Ϊ', 'Ι')
                    month_en = inv_map[GREEK_MONTHS_MAP[gr_month]]
                    year_out = match.group(2)

            lines = page_text.split('\n')
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 3:
                    if re.match(r'^[Α-ΩA-Z_\.\(\)\-]+$', parts[0]) and re.match(r'^-?\d+[\.,]?\d*$', parts[1]):
                        station = parts[0]
                        vals = [p.replace(',', '.') for p in parts[1:]]
                        
                        while len(vals) < 7:
                            vals.append("")
                            
                        all_data_rows.append({
                            "Έτος": int(year_out) if year_out != "UNKNOWN" else year_out,
                            "Μήνας": month_en,
                            "ΣΤΑΘΜΟΣ": station,
                            "Γεωγ.Μήκος": vals[0],
                            "Γεωγ.Πλάτος": vals[1],
                            "Tmean": vals[2],
                            "TX": vals[3],
                            "TN": vals[4],
                            "RR": vals[5],
                            "INST": vals[6]
                        })
                        
            print(f"✅ {filename} -> Επιτυχής εξαγωγή ως [{month_en} {year_out}]")
            
    except Exception as e:
        print(f"❌ Σφάλμα: {filename}: {e}")

if all_data_rows:
    df = pd.DataFrame(all_data_rows)
    month_to_num = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12, 'UNKNOWN': 13}
    df['month_num'] = df['Μήνας'].map(month_to_num)
    df = df.sort_values(by=['Έτος', 'month_num']).drop(columns=['month_num'])
    
    # Το τελικό Excel αποθηκεύεται στον γονικό φάκελο (BASE_DIR)
    output_path = os.path.join(BASE_DIR, "emy_master_clean.xlsx")
    df.to_excel(output_path, index=False)
    print(f"\n🎉 Το Master Excel δημιουργήθηκε τέλεια διαχωρισμένο! -> {output_path}")