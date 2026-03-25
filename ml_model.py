"""
SIMPLE ML MODEL FOR DISTRESS DETECTION
Uses TF-IDF + Naive Bayes (Perfect for 2nd year B.Tech)
Detects words: help, sos, emergency, danger, save, attack
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import os

class DistressDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.train_model()  # Train on startup
    
    def train_model(self):
        """TRAINING DATA - Explain in viva"""
        # Format: (text, label) where 1 = distress, 0 = normal
        training_data = [
            # DISTRESS EXAMPLES (label=1)
            ("help me", 1), ("sos emergency", 1), ("save me", 1),
            ("i am in danger", 1), ("attack help", 1), ("someone following me", 1),
            ("rape help", 1), ("kidnap danger", 1), ("hurt bad", 1),
            
            # NORMAL EXAMPLES (label=0)
            ("hello", 0), ("how are you", 0), ("good morning", 0),
            ("what time", 0), ("thanks", 0), ("bye", 0)
        ]
        
        # Step 1: Split data
        texts, labels = zip(*training_data)
        
        # Step 2: Convert text to numbers (TF-IDF)
        self.vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        X = self.vectorizer.fit_transform(texts)
        
        # Step 3: Train Naive Bayes classifier
        self.model = MultinomialNB()
        self.model.fit(X, labels)
        
        # Save model
        dump((self.model, self.vectorizer), 'distress_model.joblib')
        print("✅ ML Model trained and saved!")
    
    def predict(self, text):
        """Predict if text shows distress"""
        if not self.model:
            return False, 0.0
        
        # Convert text to numbers
        text_vector = self.vectorizer.transform([text.lower()])
        
        # Predict probability
        prob_distress = self.model.predict_proba(text_vector)[0][1]
        is_distress = self.model.predict(text_vector)[0] == 1
        
        return is_distress, prob_distress

# Create global detector
detector = DistressDetector()