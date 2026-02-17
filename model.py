import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stop_words = {
"a","an","the","and","or","is","are","was","were",
"in","on","at","to","for","of","with","by","as"
}
def preprocess(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return preprocess(text)


def rank_resumes(job_description, resumes):
    resume_texts = []
    resume_names = []

    for file in resumes:
        resume_names.append(file.filename)
        resume_texts.append(extract_text(file))

    documents = [preprocess(job_description)] + resume_texts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    scores = list(enumerate(similarity[0]))
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []
    for index, score in ranked:
        results.append((resume_names[index], round(score, 4)))

    return results