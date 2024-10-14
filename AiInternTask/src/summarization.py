# from transformers import pipeline

# class Summarizer:
#     def __init__(self, model_name="facebook/bart-large-cnn"):
#         # Load a pre-trained summarization model from Hugging Face
#         self.summarizer = pipeline("summarization", model=model_name)

#     def summarize(self, text, max_length=130, min_length=30):
#         try:
#             input_length = len(text.split())
#             # Set max_length to a reasonable value based on input length
#             max_length = min(max_length, max(10, int(input_length * 0.8)))  # 80% of the input length or at least 10
            
#             # Ensure min_length doesn't exceed max_length
#             min_length = min(min_length, max_length - 10)  # Maintain a gap between min and max

#             # Generate a summary for the provided text
#             summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
#             return summary[0]['summary_text']
#         except Exception as e:
#             print(f"Error during summarization: {e}")
#             return None


# # def chunk_text(text, max_chunk_size=1024):
# #     """
# #     Chunk the text into smaller pieces based on word count.
    
# #     Args:
# #     - text (str): The full text to be chunked.
# #     - max_chunk_size (int): Maximum size of each chunk in terms of word count.
    
# #     Returns:
# #     - chunks (list): List of text chunks.
# #     """
# #     words = text.split()
# #     chunks = []
# #     for i in range(0, len(words), max_chunk_size):
# #         chunks.append(" ".join(words[i:i + max_chunk_size]))
# #     return chunks

# def chunk_text(text, max_chunk_size=1024):
#     """
#     Chunk the text into smaller pieces based on word count.
    
#     Args:
#     - text (str): The full text to be chunked.
#     - max_chunk_size (int): Maximum size of each chunk in terms of word count.
    
#     Returns:
#     - chunks (list): List of text chunks.
#     """
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), max_chunk_size):
#         chunk = " ".join(words[i:i + max_chunk_size])
#         if chunk:  # Ensure chunk is not empty
#             chunks.append(chunk)
#     return chunks



# # ======================================
# # def generate_summary_for_pdf_text(text):
# #     """
# #     Generate a summary for the given PDF text by processing it in chunks if necessary.
    
# #     Args:
# #     - text (str): The full text extracted from a PDF.
    
# #     Returns:
# #     - summary (str): The combined summary generated from all chunks of the text.
# #     """
# #     num_words = len(text.split())
    
# #     if num_words < 300:
# #         # Short summary for short documents
# #         return Summarizer().summarize(text, max_length=50, min_length=20)
# #     elif 300 <= num_words < 1000:
# #         # Medium summary for medium-sized documents
# #         return Summarizer().summarize(text, max_length=100, min_length=50)
# #     else:
# #         # Long document, use chunking
# #         chunks = chunk_text(text)
# #         summarizer = Summarizer()
# #         # Summarize each chunk and combine the summaries
# #         summaries = [summarizer.summarize(chunk, max_length=200, min_length=80) for chunk in chunks]
# #         return " ".join(summaries)

# # def generate_summary_for_pdf_text(text):
# #     """
# #     Generate a summary for the given PDF text by processing it in chunks if necessary.
    
# #     Args:
# #     - text (str): The full text extracted from a PDF.
    
# #     Returns:
# #     - summary (str): The combined summary generated from all chunks of the text.
# #     """
# #     num_words = len(text.split())
    
# #     summarizer = Summarizer()
    
# #     if num_words < 300:
# #         # Short summary for short documents
# #         summary = summarizer.summarize(text, max_length=50, min_length=20)
# #         return summary if summary else ""
    
# #     elif 300 <= num_words < 1000:
# #         # Medium summary for medium-sized documents
# #         summary = summarizer.summarize(text, max_length=100, min_length=10)
# #         return summary if summary else ""

# #     else:
# #         # Long document, use chunking
# #         chunks = chunk_text(text)
# #         summaries = []
        
# #         for chunk in chunks:
# #             summary = summarizer.summarize(chunk, max_length=64, min_length=10)
# #             if summary:
# #                 summaries.append(summary)
        
# #         # Join only non-None summaries
# #         return " ".join([s for s in summaries if s])


# def generate_summary_for_pdf_text(text):
#     """
#     Generate a summary for the given PDF text by processing it in chunks if necessary.
    
#     Args:
#     - text (str): The full text extracted from a PDF.
    
#     Returns:
#     - summary (str): The combined summary generated from all chunks of the text.
#     """
#     num_words = len(text.split())
    
#     summarizer = Summarizer()
    
#     if num_words < 300:
#         # Short summary for short documents
#         summary = summarizer.summarize(text, max_length=50, min_length=20)
#         return summary if summary else ""
    
#     elif 300 <= num_words < 1000:
#         # Medium summary for medium-sized documents
#         summary = summarizer.summarize(text, max_length=100, min_length=10)
#         return summary if summary else ""

#     else:
#         # Long document, use chunking
#         chunks = chunk_text(text)
#         summaries = []
        
#         for chunk in chunks:
#             try:
#                 summary = summarizer.summarize(chunk, max_length=64, min_length=10)
#                 if summary:
#                     summaries.append(summary)
#             except Exception as e:
#                 print(f"Error during summarization of chunk: {e}")
        
#         # Join only non-None summaries
#         return " ".join([s for s in summaries if s])


# ================================================================
# from transformers import pipeline

# class Summarizer:
#     def __init__(self, model_name="facebook/bart-large-cnn"):
#         # Load a pre-trained summarization model from Hugging Face
#         self.summarizer = pipeline("summarization", model=model_name)

#     def summarize(self, text, max_length=130, min_length=30):
#         try:
#             input_length = len(text.split())
#             # Set max_length to a reasonable value based on input length
#             max_length = min(max_length, max(10, int(input_length * 0.8)))  # 80% of the input length or at least 10
            
#             # Ensure min_length doesn't exceed max_length
#             min_length = min(min_length, max_length - 10)  # Maintain a gap between min and max

#             # Generate a summary for the provided text
#             summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
#             return summary[0]['summary_text']
#         except Exception as e:
#             print(f"Error during summarization: {e}")
#             return None

# def chunk_text(text, max_chunk_size=1024):
#     """
#     Chunk the text into smaller pieces based on word count.
    
#     Args:
#     - text (str): The full text to be chunked.
#     - max_chunk_size (int): Maximum size of each chunk in terms of word count.
    
#     Returns:
#     - chunks (list): List of text chunks.
#     """
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), max_chunk_size):
#         chunk = " ".join(words[i:i + max_chunk_size])
#         if chunk:  # Ensure chunk is not empty
#             chunks.append(chunk)
#     return chunks


# def generate_summary_for_pdf_text(text):
#     """
#     Generate a summary for the given PDF text by processing it in chunks if necessary.
    
#     Args:
#     - text (str): The full text extracted from a PDF.
    
#     Returns:
#     - summary (str): The combined summary generated from all chunks of the text.
#     """
#     num_words = len(text.split())
    
#     summarizer = Summarizer()
    
#     if num_words < 300:
#         # Short summary for short documents
#         summary = summarizer.summarize(text, max_length=50, min_length=20)
#         return summary if summary else ""
    
#     elif 300 <= num_words < 1000:
#         # Medium summary for medium-sized documents
#         summary = summarizer.summarize(text, max_length=100, min_length=10)
#         return summary if summary else ""

#     else:
#         # Long document, use chunking
#         chunks = chunk_text(text)
#         summaries = []
        
#         for chunk in chunks:
#             try:
#                 summary = summarizer.summarize(chunk, max_length=64, min_length=10)
#                 if summary:
#                     summaries.append(summary)
#             except Exception as e:
#                 print(f"Error during summarization of chunk: {e}")
        
#         # Join only non-None summaries
#         return " ".join([s for s in summaries if s])

# =====================================================

# from transformers import T5ForConditionalGeneration, T5Tokenizer
# import torch

# class Summarizer:
#     def __init__(self, model_name="t5-base"):
#         # Load pre-trained model and tokenizer
#         self.tokenizer = T5Tokenizer.from_pretrained(model_name)
#         self.model = T5ForConditionalGeneration.from_pretrained(model_name)

#     def summarize(self, text, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, no_repeat_ngram_size=2):
#         """
#         Summarize the input text using T5 model.
#         """
#         # Preprocess the input text for T5
#         input_ids = self.tokenizer.encode(f"summarize: {text}", return_tensors="pt", max_length=512, truncation=True)
        
#         # Generate the summary (Greedy or Beam search depending on parameters)
#         summary_ids = self.model.generate(
#             input_ids, 
#             max_length=max_length, 
#             min_length=min_length, 
#             length_penalty=length_penalty, 
#             num_beams=num_beams, 
#             no_repeat_ngram_size=no_repeat_ngram_size, 
#             early_stopping=True
#         )
        
#         # Decode the summary output
#         summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#         return summary

# ==========================================================

from transformers import T5ForConditionalGeneration, T5Tokenizer

class Summarizer:
    def __init__(self, model_name="t5-base"):
        # Load pre-trained model and tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, no_repeat_ngram_size=2):
        """
        Summarize the input text using T5 model.
        """
        # Preprocess the input text for T5
        input_ids = self.tokenizer.encode(f"summarize: {text}", return_tensors="pt", max_length=512, truncation=True)
        
        # Generate the summary
        summary_ids = self.model.generate(
            input_ids, 
            max_length=max_length, 
            min_length=min_length, 
            length_penalty=length_penalty, 
            num_beams=num_beams, 
            no_repeat_ngram_size=no_repeat_ngram_size, 
            early_stopping=True
        )
        
        # Decode the summary output
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

# Create a function for easy import
def summarize(text):
    summarizer = Summarizer()
    return summarizer.summarize(text)
