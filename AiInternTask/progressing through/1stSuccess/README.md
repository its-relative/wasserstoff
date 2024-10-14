Here is the README in Markdown (.md) format:
Wasserstoff AI Intern Task
==========================
Domain-Specific PDF Summarization & Keyword Extraction Pipeline
-------------------------------------------------------------
[!]()
[!]()
[!](LICENSE)
Table of Contents
-----------------

Overview
------------
This project develops a robust pipeline to process PDF documents, generating dynamic summaries and extracting domain-specific keywords using custom algorithms.
Features
------------

    Concurrent PDF processing
    Dynamic summarization
    TF-IDF/YAKE keyword extraction
    MongoDB storage
    Performance metrics

Requirements
---------------

    Python 3.x
    MongoDB 4.x
    Required libraries: requirements.txt

Installation
---------------

    Clone repository: git clone git@github.com:its-relative/sapeksh-tomar-wasserstoff-AiInternTask.git
    Install dependencies: pip install -r requirements.txt
    Set up MongoDB

Usage
---------

    Add PDF files to pdfs/ directory
    Run pipeline: python src/main.py
    View results in MongoDB

Pipeline Architecture
-----------------------

pdfs/
  ├── input_pdf1.pdf
  ├── input_pdf2.pdf
  └── ...
output/
  ├── summary_pdf1.txt
  ├── summary_pdf2.txt
  └── ...
logs/
  ├── log_file.log
  └── ...
src/
  ├── pdf_ingestion.py
  ├── summarization.py
  ├── keyword_extraction.py
  ├── db_operations.py
  └── main.py
requirements.txt
LICENSE
README.md

Contributing
---------------
Contributions are welcome!
License
---------
This project is licensed under the MIT License.