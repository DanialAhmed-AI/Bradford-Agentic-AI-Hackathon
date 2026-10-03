from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class MLModel:
    """
    Small supervised NLP classifier used by the agent to identify intent.
    This is intentionally simple so it can be trained and explained during
    a one-day hackathon.
    """

    def __init__(self):
        texts = [
            "best laptop for computer science",
            "recommend a laptop under 800 pounds",
            "which computer should I buy",
            "laptop for programming students",
            "cheap laptop for coding",
            "find me a laptop for university",
            "compare laptops under 800",
            "best laptop for students under 700",
            "portable laptop with long battery life",
            "lightweight laptop for travel and university",
            "best budget laptop for software engineering",
            "laptop for machine learning students",
            "best performance laptop for coding and video editing",
            "what is machine learning",
            "explain artificial intelligence",
            "what is quantum computing",
            "tell me about neural networks",
            "how does deep learning work",
            "what is supervised learning",
            "compare ai and ml",
        ]

        labels = [
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "laptop_recommendation",
            "general_ai",
            "general_ai",
            "general_ai",
            "general_ai",
            "general_ai",
            "general_ai",
            "general_ai",
        ]

        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000))
        ])
        self.model.fit(texts, labels)

    def predict(self, text: str):
        prediction = self.model.predict([text])[0]
        probabilities = self.model.predict_proba([text])[0]
        confidence = float(max(probabilities))
        return {"prediction": prediction, "confidence": confidence}
