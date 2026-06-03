# EMY Climate Data ETL Pipeline 🌤️

An automated ETL (Extract, Transform, Load) pipeline built in Python to download, parse, and clean climatological data from the Hellenic National Meteorological Service (EMY) legacy portal. 

This project downloads monthly climate bulletins (PDFs), intelligently targets the relevant data pages, extracts tabular meteorological metrics using RegEx, and compiles everything into a clean, structured Master Excel file.

## 🚀 Features

* **Automated PDF Scraping:** Iterates through EMY portal file IDs to download monthly climate reports, with built-in retry logic and error handling.
* **Smart PDF Trimming:** Extracts only the necessary page (Page 4, or the last page depending on document length) to save space and processing time.
* **Intelligent Naming & Mapping:** Automatically parses messy filename headers and standardizes them into a clean `MMM_YYYY.pdf` format.
* **Regex-Powered Data Extraction:** Uses `pdfplumber` to read unstructured PDF text, parsing Greek month names and extracting key meteorological data points.
* **Master Excel Export:** Compiles all historical data into a neatly sorted, ready-to-analyze `.xlsx` file using `pandas`.

## 🛠️ Prerequisites

Ensure you have Python 3.7+ installed. You will need the following libraries:

    pip install requests pypdf pdfplumber pandas openpyxl

## 📂 Project Structure

* `etl_emy_pipeline.py`: The extraction script. Connects to the EMY portal, downloads the PDFs, trims them to the relevant page, and saves them locally.
* `extract_to_excel.py`: The transformation and loading script. Reads the downloaded PDFs, extracts the tabular data, and exports a final master Excel file.

## ⚙️ How to Use

1. **Clone the repository:**

    git clone https://github.com/TsakalParis/EMY_ETL.git
    cd emy-climate-etl

2. **Run the Downloader:**
   This will create an `EMY_DATA/pdf` directory and populate it with the parsed PDF pages.

    python etl_emy_pipeline.py

3. **Run the Extractor:**
   This will read all PDFs in the directory and generate `emy_master_clean.xlsx`.

    python extract_to_excel.py

## 📊 Data Output Structure

The final `emy_master_clean.xlsx` contains the following columns extracted from the EMY bulletins:

| Column Header | Description |
| :--- | :--- |
| **Έτος** | Year |
| **Μήνας** | Month (Standardized to 3-letter English, e.g., JAN) |
| **ΣΤΑΘΜΟΣ** | Weather Station Name (Greek) |
| **Γεωγ.Μήκος** | Longitude |
| **Γεωγ.Πλάτος** | Latitude |
| **Tmean** | Mean Temperature (°C) |
| **TX** | Maximum Temperature (°C) |
| **TN** | Minimum Temperature (°C) |
| **RR** | Total Rainfall/Precipitation (mm) |
| **INST** | Maximum Wind Gust |

## ⚠️ Disclaimer

This is an unofficial tool created for educational and data analysis purposes. It interacts with the public, legacy portal of the Hellenic National Meteorological Service (EMY). Please ensure your scraping frequency (handled via `time.sleep()` in the code) remains respectful to their server loads.
