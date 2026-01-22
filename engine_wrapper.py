import torch
import joblib
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class ProfessionalTicketEngine:
    def __init__(self, bert_path, svm_path, tfidf_path):
        # Load BERT
        self.tokenizer = AutoTokenizer.from_pretrained(bert_path)
        self.bert_model = AutoModelForSequenceClassification.from_pretrained(bert_path)
        
        # Load SVM & TF-IDF
        self.svm_model = joblib.load(svm_path)
        self.tfidf = joblib.load(tfidf_path)
        
        # Category Mapping - MUST match training labels from M3.ipynb
        self.categories = ['Access', 'Administrative rights', 'Hardware', 'HR Support', 
                          'Internal Project', 'Miscellaneous', 'Purchase', 'Storage']
    
    def process_ticket(self, text):
        # Validate input length
        if len(text.strip()) < 10:
            return {
                "category": "Miscellaneous",
                "confidence": 0.0,
                "urgency": "Standard",
                "error": "Input too short. Please provide at least 10 characters for proper categorization."
            }
        
        # --- 1. SVM Prediction (TF-IDF) ---
        tfidf_feat = self.tfidf.transform([text])
        svm_probs = self.svm_model.predict_proba(tfidf_feat)[0]
        
        # --- 2. BERT Prediction ---
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            bert_logits = self.bert_model(**inputs).logits
            # Use torch.softmax like M3.ipynb for consistency
            bert_probs = torch.softmax(bert_logits, dim=1).numpy()[0]
        
        # --- 3. Weighted Soft Voting (60% BERT, 40% SVM) ---
        final_probs = (0.6 * bert_probs) + (0.4 * svm_probs)
        category_idx = np.argsort(final_probs)[-1]  # Get index of max probability
        confidence = float(final_probs[category_idx])  # Keep as decimal (0-1), not percentage
        
        # --- 4. CONFIDENCE THRESHOLDS (from M3.ipynb) ---
        HIGH_CONF = 0.70   # 70%
        LOW_CONF = 0.45    # 45%
        
        if confidence >= HIGH_CONF:
            final_category = self.categories[category_idx]
            ticket_status = "Auto-Categorized"
        elif confidence >= LOW_CONF:
            final_category = self.categories[category_idx]
            ticket_status = "Pending Verification"
        else:
            final_category = "Miscellaneous"
            ticket_status = "Requires Manual Review"
        
        # --- 5. URGENCY DETECTION ---
        urgent_keywords = ['urgent', 'broken', 'emergency', 'critical', 'down', 'outage', 'crash', 'severe', 'flickering']
        urgency = "High" if any(word in text.lower() for word in urgent_keywords) else "Standard"
        
        # --- 6. RETURN RESULT ---
        return {
            "category": final_category,
            "confidence": round(confidence * 100, 2),  # Convert to percentage for display
            "urgency": urgency,
            "status": ticket_status
        }