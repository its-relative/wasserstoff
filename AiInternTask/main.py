import os
import requests
import pdfplumber
from multiprocessing import Pool
import time
import psutil

# from src.summarization import generate_summary_for_pdf_text  # Corrected import
from src.summarization import summarize
from src.keyword_extraction import extract_keywords_from_pdf_text  # Corrected import
from src.db_operations import connect_to_mongo, store_pdf_data

# Directory for downloading PDFs
download_dir = 'downloaded_pdfs'

# PDF links to download and process
pdf_links = {
  "pdf1": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTUwL3ZvbHVtZSAxL1BhcnQgSS9Db21taXNzaW9uZXIgb2YgSW5jb21lIFRheCwgV2VzdCBCZW5nYWxfQ2FsY3V0dGEgQWdlbmN5IEx0ZC5fMTY5NzYwNjMxMC5wZGY=",
  "pdf2": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTUyL3ZvbHVtZSAxL1BhcnQgSS90aGUgc3RhdGUgb2YgYmloYXJfbWFoYXJhamFkaGlyYWphIHNpciBrYW1lc2h3YXIgc2luZ2ggb2YgZGFyYmhhbmdhIGFuZCBvdGhlcnNfMTY5ODMxODQ0OC5wZGY=",
  "pdf3": "https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2024/07/20240716890312078.pdf",
  "pdf4": "https://www.mha.gov.in/sites/default/files/250883_english_01042024.pdf",
  "pdf5": "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR60974A2ED1DFDB84EC0B3AABFB8419E1431.PDF",
  "pdf6": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgdGF0YSBvaWwgbWlsbHMgY28uIGx0ZC5faXRzIHdvcmttZW4gYW5kIG90aGVyc18xNjk5MzMzODYyLnBkZg==",
  "pdf7": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9ncmVhdCBpbmRpYW4gbW90b3Igd29ya3MgbHRkLiwgYW5kIGFub3RoZXJfdGhlaXIgZW1wbG95ZWVzIGFuZCBvdGhlcnNfMTY5OTMzNjM1NS5wZGY=",
  "pdf8": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9tZXNzcnMuIGlzcGFoYW5pIGx0ZC4gY2FsY3V0dGFfaXNwYWhhbmkgZW1wbG95ZWVzICB1bmlvbl8xNjk5MzM4NTQ5LnBkZg==",
  "pdf9": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9waHVsYmFyaSB0ZWEgZXN0YXRlX2l0cyB3b3JrbWVuXzE2OTkzMzkyMjYucGRm",
  "pdf10": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgbG9yZCBrcmlzaG5hIHN1Z2FyIG1pbGxzIGx0ZC4sIGFuZCBhbm90aGVyX3RoZSB1bmlvbiBvZiBpbmRpYSBhbmQgYW5vdGhlcl8xNjk5MzQxMDE0LnBkZg==",
  "pdf11": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS8xNjk5NTIxMzUwLnBkZg==",
  "pdf12": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgZ3JhaGFtIHRyYWRpbmcgY28uIChpbmRpYSkgbHRkLl9pdHMgd29ya21lbl8xNjk5NTIzNTc3LnBkZg==",
  "pdf13": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgY29tbWlzc2lvbmVyIG9mIGluY29tZS10YXgsIGJvbWJheV9yYW5jaGhvZGRhcyBrYXJzb25kYXMsIGJvbWJheV8xNjk5NTI2MjI3LnBkZg==",
  "pdf14": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS8xNjk5NTI2ODA0LnBkZg==",
  "pdf15": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9zaHJpIGIuIHAuIGhpcmEsIHdvcmtzIG1hbmFnZXIsIGNlbnRyYWwgcmFpbHdheSwgcGFyZWwsIGJvbWJheSBldGMuX3NocmkgYy4gbS4gcHJhZGhhbiBldGMuXzE2OTk1MjcyMTcucGRm",
  "pdf16": "https://www.sebi.gov.in/sebi_data/attachdocs/1292585113260.pdf",
  "pdf17": "https://ijtr.nic.in/Circular%20Orders%20(Supplement).pdf",
  "pdf18": "https://enforcementdirectorate.gov.in/sites/default/files/Act%26rules/The%20Prevention%20of%20Money-laundering%20%28Maintenance%20of%20Records%29%20Rules%2C%202005.pdf"
}

# Initialize MongoDB connection
db = connect_to_mongo()

# Ensure download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

def download_pdf(pdf_name, url):
    """
    Download PDF from a given URL and save it to the download directory.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(download_dir, f"{pdf_name}.pdf")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"{pdf_name} downloaded successfully.")
            return file_path
        else:
            print(f"Failed to download {pdf_name}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {pdf_name}: {e}")
        return None

def process_pdf(file_name, file_path):
    """
    Process a single PDF file: extract text, summarize, extract keywords, and store in MongoDB.
    """
    print(f"Processing file: {file_name}")
    
    start_time = time.time()

    # Extract text from PDF
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    if text:
        # Summarize the text
        # summary = generate_summary_for_pdf_text(text)  # Corrected function call
        summary = summarize(text)

        # Extract keywords
        keywords = extract_keywords_from_pdf_text(text)  # Corrected function call
        
        # Store results in MongoDB
        store_pdf_data(db, file_name, summary, keywords)
        print(f"Successfully processed and stored {file_name}")
    else:
        print(f"No text extracted from {file_name}")

    # Performance metrics
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    execution_time = time.time() - start_time  # Calculate time taken
    
    print(f"Performance metrics for {file_name}:")
    print(f"Memory Usage: {memory_usage:.2f} MB")
    print(f"Time Taken: {execution_time:.2f} seconds")

    return execution_time
def process_all_pdfs(pdf_links):
    """
    Download and process all PDFs from the provided dictionary of links.
    """
    total_time = 0
    for pdf_name, url in pdf_links.items():
        file_path = download_pdf(pdf_name, url)
        if file_path:
            total_time += process_pdf(pdf_name, file_path)
    print(f"Total Time for processing all PDFs: {total_time:.2f} seconds")

def process_pdfs_from_folder(folder_path):
    """
    Process all PDF files in the specified folder.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            process_pdf(filename, file_path)


def process_pdfs_concurrently(pdf_links):
    """
    Process all PDFs concurrently using multiprocessing, logging performance data.
    """
    start_time = time.time()
    with Pool() as pool:
        pool.map(process_pdf_wrapper, pdf_links.items())  # process multiple PDFs concurrently
    total_time = time.time() - start_time
    
    print(f"Total time for concurrent processing: {total_time:.2f} seconds")

def process_pdf_wrapper(item):
    pdf_name, url = item
    file_path = download_pdf(pdf_name, url)
    if file_path:
        process_pdf(pdf_name, file_path)

def get_pdf_folder():
    """
    Prompt the user to input the folder path containing PDFs.
    """
    folder_path = input("Enter the path to the folder containing PDFs: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return folder_path
    else:
        print(f"Invalid folder path: {folder_path}")
        return None

def list_pdfs_in_folder(folder_path):
    """
    List all PDF files in the specified folder.
    """
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if pdf_files:
        print(f"Found {len(pdf_files)} PDF files in {folder_path}")
    else:
        print(f"No PDF files found in {folder_path}")
    return pdf_files

def process_pdfs_from_folder(folder_path):
    """
    Process all PDF files from a folder.
    """
    total_time = 0
    pdf_files = list_pdfs_in_folder(folder_path)
    
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        total_time += process_pdf(pdf_file, file_path)
    
    print(f"Total time for processing all PDFs in the folder: {total_time:.2f} seconds")


if __name__ == "__main__":
    # Process all PDF links provided
    process_all_pdfs(pdf_links)
    print("All PDFs processed successfully!")

# Concurrent Processing
    print("Processing PDFs Concurrently...")
    process_pdfs_concurrently(pdf_links)

# Ask the user for the folder path
    folder_path = get_pdf_folder()

    if folder_path:
        process_pdfs_from_folder(folder_path)
    else:
        print("No valid folder path provided. Exiting.")
