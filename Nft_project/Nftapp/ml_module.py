import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters, numbers, and extra whitespaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())

    return text

# Function to load and train the model
def train_model():
    # Load your dataset (assumed to have columns 'Resume_str' and 'Category')
    df = pd.read_csv('Nftapp/Resume.csv')

    # Apply preprocessing to 'Resume_str' column
    df['Resume_str'] = df['Resume_str'].apply(preprocess_text)

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    # Feature extraction using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train = tfidf_vectorizer.fit_transform(train_data['Resume_str'])

    # Create labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_data['Category'])

    # Train a RandomForestClassifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    return rf_classifier, tfidf_vectorizer, label_encoder

# Function to rank resumes based on a job description
def rank_resumes(job_description, rf_classifier, tfidf_vectorizer, label_encoder, applicants):
    job_description = preprocess_text(job_description)
    job_description_tfidf = tfidf_vectorizer.transform([job_description])

    # Make predictions for ranking
    ranking_scores = rf_classifier.predict_proba(job_description_tfidf)[:, 1]

    # Update ranking scores in the Applicant model
    for applicant, ranking_score in zip(applicants, ranking_scores):
        print(f"Applicant: {applicant.name}, Ranking Score: {ranking_score}")
        applicant.ranking_score = ranking_score
        applicant.save()

    return ranking_scores