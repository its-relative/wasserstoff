from transformers import pipeline

class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        # Load a pre-trained summarization model from Hugging Face
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, max_length=130, min_length=30):
        try:
            # Generate a summary for the provided text
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error during summarization: {e}")
            return None

def generate_summary_for_pdf_text(text):
    # Length of the text can be used to adjust summarization length
    num_words = len(text.split())
    
    if num_words < 300:
        # Short summary for short documents
        return Summarizer().summarize(text, max_length=50, min_length=20)
    elif 300 <= num_words < 1000:
        # Medium summary for medium-sized documents
        return Summarizer().summarize(text, max_length=100, min_length=50)
    else:
        # Long summary for long documents
        return Summarizer().summarize(text, max_length=200, min_length=80)
