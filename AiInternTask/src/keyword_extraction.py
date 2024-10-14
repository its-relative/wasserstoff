from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordExtractor:
    def __init__(self, max_keywords=10):
        # Adjusted max_df to 1.0 for single document processing
        self.max_keywords = max_keywords
        self.vectorizer = TfidfVectorizer(stop_words='english', max_df=1.0, min_df=1)  # Changed max_df

    def clean_text(self, text):
        # Clean the text by removing special characters and numbers
        text = re.sub(r'\d+', '', text)  # remove numbers
        text = re.sub(r'\W+', ' ', text)  # remove special characters
        return text

    def extract_keywords(self, text):
        # Clean the input text
        cleaned_text = self.clean_text(text)
        
        # Fit and transform the text using TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform([cleaned_text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Sort TF-IDF scores for keywords
        scores = tfidf_matrix.toarray()[0]
        keyword_indices = scores.argsort()[-self.max_keywords:][::-1]
        keywords = [feature_names[index] for index in keyword_indices]
        
        return keywords

    def get_embeddings(self, text):
        """
        Get BERT embeddings for the given text.
        """
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state  # Embeddings for each token

    def compare_embeddings(self, text1, text2):
        """
        Compare embeddings of two texts by computing the cosine similarity.
        """
        embeddings1 = self.get_embeddings(text1).mean(dim=1).numpy()  # Average over tokens
        embeddings2 = self.get_embeddings(text2).mean(dim=1).numpy()  # Average over tokens
        similarity_score = cosine_similarity(embeddings1, embeddings2)
        return similarity_score[0][0]  # Return the similarity score as a scalar

# Standalone function for extracting keywords using BERT
def extract_keywords_from_pdf_text(text):
    extractor = KeywordExtractor(max_keywords=10)
    return extractor.extract_keywords(text)
