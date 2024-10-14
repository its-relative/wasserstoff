# # import os
# # # import textract
# # from PyPDF2 import PdfReader
# # import pdfplumber
# # from pymongo import MongoClient

# # # from summarization import summarize_text

# # from src.summarization import summarize_text
# # from src.keyword_extraction import extract_keywords

# # # from keyword_extraction import extract_keywords

# # # Initialize MongoDB connection
# # client = MongoClient("mongodb://localhost:27017/")
# # db = client["pdf_summary_db"]
# # collection = db["pdf_documents"]

# # # Define the base directory containing the PDFs
# # base_dir = 'pdfs/'

# # # Function to read PDFs using pdfplumber for better accuracy
# # def read_pdf(file):
# #     try:
# #         with pdfplumber.open(file) as pdf:
# #             text = ''
# #             for page in pdf.pages:
# #                 text += page.extract_text() if page.extract_text() else ''
# #         return text
# #     except Exception as e:
# #         print(f'Error reading PDF {file}: {e}')
# #         return None

# # # Walk through the directory structure and process PDFs
# # for root, dirs, files in os.walk(base_dir):
# #     for file_name in files:
# #         # Print the file name for debugging purposes
# #         print(f'Processing file: {file_name}')
        
# #         # Get the file path
# #         file_path = os.path.join(root, file_name)
        
# #         # Handle only PDFs in this case
# #         if file_name.endswith('.pdf'):
# #             content = read_pdf(file_path)
# #         else:
# #             print(f'Skipping file: {file_name} (unsupported format)')
# #             continue
        
# #         if content is not None:
# #             # Summarize the text
# #             summary = summarize_text(content, method="textrank")  # You can use the transformer-based method here
            
# #             # Extract keywords from the text
# #             keywords = extract_keywords(content, num_keywords=5)
            
# #             # Store the results in MongoDB
# #             document = {
# #                 "pdf_name": file_name,
# #                 "summary": summary,
# #                 "keywords": keywords
# #             }
# #             collection.insert_one(document)
# #             print(f'Successfully processed and saved {file_name}')
# #         else:
# #             print(f'Failed to read file {file_name}. Content is None.')

# # print('PDF processing complete, summaries and keywords saved to MongoDB successfully!')


# import requests
# import os

# # Dictionary of PDF links
# pdf_links = {
#   "pdf1": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTUwL3ZvbHVtZSAxL1BhcnQgSS9Db21taXNzaW9uZXIgb2YgSW5jb21lIFRheCwgV2VzdCBCZW5nYWxfQ2FsY3V0dGEgQWdlbmN5IEx0ZC5fMTY5NzYwNjMxMC5wZGY=",
#   "pdf2": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTUyL3ZvbHVtZSAxL1BhcnQgSS90aGUgc3RhdGUgb2YgYmloYXJfbWFoYXJhamFkaGlyYWphIHNpciBrYW1lc2h3YXIgc2luZ2ggb2YgZGFyYmhhbmdhIGFuZCBvdGhlcnNfMTY5ODMxODQ0OC5wZGY=",
#   "pdf3": "https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2024/07/20240716890312078.pdf",
#   "pdf4": "https://www.mha.gov.in/sites/default/files/250883_english_01042024.pdf",
#   "pdf5": "https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR60974A2ED1DFDB84EC0B3AABFB8419E1431.PDF",
#   "pdf6": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgdGF0YSBvaWwgbWlsbHMgY28uIGx0ZC5faXRzIHdvcmttZW4gYW5kIG90aGVyc18xNjk5MzMzODYyLnBkZg==",
#   "pdf7": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9ncmVhdCBpbmRpYW4gbW90b3Igd29ya3MgbHRkLiwgYW5kIGFub3RoZXJfdGhlaXIgZW1wbG95ZWVzIGFuZCBvdGhlcnNfMTY5OTMzNjM1NS5wZGY=",
#   "pdf8": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9tZXNzcnMuIGlzcGFoYW5pIGx0ZC4gY2FsY3V0dGFfaXNwYWhhbmkgZW1wbG95ZWVzICB1bmlvbl8xNjk5MzM4NTQ5LnBkZg==",
#   "pdf9": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9waHVsYmFyaSB0ZWEgZXN0YXRlX2l0cyB3b3JrbWVuXzE2OTkzMzkyMjYucGRm",
#   "pdf10": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgbG9yZCBrcmlzaG5hIHN1Z2FyIG1pbGxzIGx0ZC4sIGFuZCBhbm90aGVyX3RoZSB1bmlvbiBvZiBpbmRpYSBhbmQgYW5vdGhlcl8xNjk5MzQxMDE0LnBkZg==",
#   "pdf11": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS8xNjk5NTIxMzUwLnBkZg==",
#   "pdf12": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgZ3JhaGFtIHRyYWRpbmcgY28uIChpbmRpYSkgbHRkLl9pdHMgd29ya21lbl8xNjk5NTIzNTc3LnBkZg==",
#   "pdf13": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS90aGUgY29tbWlzc2lvbmVyIG9mIGluY29tZS10YXgsIGJvbWJheV9yYW5jaGhvZGRhcyBrYXJzb25kYXMsIGJvbWJheV8xNjk5NTI2MjI3LnBkZg==",
#   "pdf14": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS8xNjk5NTI2ODA0LnBkZg==",
#   "pdf15": "https://digiscr.sci.gov.in/pdf_viewer?dir=YWRtaW4vanVkZ2VtZW50X2ZpbGUvanVkZ2VtZW50X3BkZi8xOTYwL3ZvbHVtZSAxL1BhcnQgSS9zaHJpIGIuIHAuIGhpcmEsIHdvcmtzIG1hbmFnZXIsIGNlbnRyYWwgcmFpbHdheSwgcGFyZWwsIGJvbWJheSBldGMuX3NocmkgYy4gbS4gcHJhZGhhbiBldGMuXzE2OTk1MjcyMTcucGRm",
#   "pdf16": "https://www.sebi.gov.in/sebi_data/attachdocs/1292585113260.pdf",
#   "pdf17": "https://ijtr.nic.in/Circular%20Orders%20(Supplement).pdf",
#   "pdf18": "https://enforcementdirectorate.gov.in/sites/default/files/Act%26rules/The%20Prevention%20of%20Money-laundering%20%28Maintenance%20of%20Records%29%20Rules%2C%202005.pdf"
# }

# # Directory to save the downloaded PDFs
# output_dir = "downloaded_pdfs"
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# def download_pdf(pdf_name, url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             file_path = os.path.join(output_dir, f"{pdf_name}.pdf")
#             with open(file_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"{pdf_name} downloaded successfully.")
#         else:
#             print(f"Failed to download {pdf_name}. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error downloading {pdf_name}: {e}")

# # Loop over the PDF links and download each one
# for pdf_name, url in pdf_links.items():
#     download_pdf(pdf_name, url)




# import os
# import pdfplumber
# from src.summarization import summarize_text
# from src.keyword_extraction import extract_keywords
# from src.db_operations import connect_to_mongo, store_pdf_data

# # Initialize MongoDB connection
# db = connect_to_mongo()

# # Directory containing PDFs
# pdf_dir = 'pdfs'

# def process_pdf(file_name, file_path):
#     """
#     Process a single PDF file: extract text, summarize, extract keywords, and store in MongoDB.
#     """
#     print(f"Processing file: {file_name}")
    
#     # Extract text from PDF
#     with pdfplumber.open(file_path) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text() or ''

#     if text:
#         # Summarize the text using TextRank
#         summary = summarize_text(text, method="textrank")
        
#         # Extract keywords using TF-IDF (or YAKE)
#         keywords = extract_keywords(text, num_keywords=5)
        
#         # Store results in MongoDB
#         store_pdf_data(db, file_name, summary, keywords)
#         print(f"Successfully processed and stored {file_name}")
#     else:
#         print(f"No text extracted from {file_name}")

# # Process all PDFs in the directory
# def process_all_pdfs(pdf_dir):
#     """
#     Process all PDFs in the specified directory.
#     """
#     for root, dirs, files in os.walk(pdf_dir):
#         for file_name in files:
#             if file_name.endswith('.pdf'):
#                 file_path = os.path.join(root, file_name)
#                 process_pdf(file_name, file_path)

# if __name__ == "__main__":
#     # Process all PDFs in the directory
#     process_all_pdfs(pdf_dir)
#     print("All PDFs processed successfully!")
