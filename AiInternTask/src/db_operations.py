from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(filename="logs/db_operations.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

def connect_to_mongo(db_name="pdf_database", collection_name="pdf_data"):
    """
    Connect to the MongoDB instance and return the collection.
    """
    try:
        # Set up the MongoDB client (ensure MongoDB is running on localhost:27017 or update with your connection string)
        client = MongoClient("mongodb://localhost:27017/")
        
        # Access the specified database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        logging.info(f"Connected to MongoDB database: {db_name}, collection: {collection_name}")
        return collection
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return None

def store_pdf_data(collection, file_name, summary, keywords):
    """
    Store the extracted data from PDF (file name, summary, keywords) into MongoDB.
    """
    try:
        # Create the document structure to be inserted into MongoDB
        document = {
            "file_name": file_name,
            "summary": summary,
            "keywords": keywords
        }
        
        # Insert the document into MongoDB
        result = collection.insert_one(document)
        
        logging.info(f"Inserted document into MongoDB with id: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error storing PDF data in MongoDB: {e}")

