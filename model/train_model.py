import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

data = pd.read_csv("../dataset/resume_data.csv")

X = data["Resume_Text"]
y = data["Category"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, stop_words="english")),
    ("clf", MultinomialNB())
])

pipeline.fit(X, y)

pickle.dump(pipeline, open("resume_model.pkl", "wb"))
print("✅ ML Pipeline Model Saved")
