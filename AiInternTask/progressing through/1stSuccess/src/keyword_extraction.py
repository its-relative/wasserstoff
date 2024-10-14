# from sklearn.feature_extraction.text import TfidfVectorizer
# import re

# class KeywordExtractor:
#     def __init__(self, max_keywords=10):
#         # Initialize parameters for keyword extraction
#         self.max_keywords = max_keywords
#         self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.85)

#     def clean_text(self, text):
#         # Clean the text by removing special characters and numbers
#         text = re.sub(r'\d+', '', text)  # remove numbers
#         text = re.sub(r'\W+', ' ', text)  # remove special characters
#         return text

#     def extract_keywords(self, text):
#         # Clean the input text
#         cleaned_text = self.clean_text(text)
        
#         # Fit and transform the text using TF-IDF
#         tfidf_matrix = self.vectorizer.fit_transform([cleaned_text])
#         feature_names = self.vectorizer.get_feature_names_out()
        
#         # Sort TF-IDF scores for keywords
#         scores = tfidf_matrix.toarray()[0]
#         keyword_indices = scores.argsort()[-self.max_keywords:][::-1]
#         keywords = [feature_names[index] for index in keyword_indices]
        
#         return keywords

# def extract_keywords_from_pdf_text(text):
#     extractor = KeywordExtractor(max_keywords=10)
#     return extractor.extract_keywords(text)


from sklearn.feature_extraction.text import TfidfVectorizer
import re

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


def extract_keywords_from_pdf_text(text):
    extractor = KeywordExtractor(max_keywords=10)
    return extractor.extract_keywords(text)