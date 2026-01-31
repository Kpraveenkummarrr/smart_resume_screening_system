import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("../dataset/resume_data.csv")

X = df["Resume_Text"]
y = df["Category"]

vectorizer = TfidfVectorizer(stop_words="english", max_features=3000)
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

pickle.dump(model, open("resume_model.pkl", "wb"))
pickle.dump(vectorizer, open("tfidf.pkl", "wb"))

print("✅ Model trained successfully")
