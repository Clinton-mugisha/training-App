import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
from .models import Applicant

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
    words = [word for word in text.split() if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join the words back into a single string
    processed_text = ' '.join(words)

    # Print debug information
    print(f"Original Text: {text}")
    print(f"Processed Text: {processed_text}")

    # Check if the processed text is empty
    if not processed_text.strip():
        print("Warning: Processed text is empty!")

    return processed_text if processed_text.strip() else 'no_content'


# Function to load and train the model
def train_model():
    # Load your dataset using the Applicant model
    applicants_data = Applicant.objects.values('name', 'cv', 'applied_job__title')
    df = pd.DataFrame.from_records(applicants_data, columns=['name', 'cv', 'applied_job__title'])

    # Debug information
    print("Number of unique categories:", df['applied_job__title'].nunique())

    # Apply preprocessing to 'cv' column
    def read_cv_content(file_path):
        print(f"Reading file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"Content read: {content}")
                return content
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""

    df['cv'] = df['cv'].apply(read_cv_content)
    df['cv'] = df['cv'].apply(preprocess_text)

    # Split the data into training and testing sets
    train_data, _ = train_test_split(df, test_size=0.2, random_state=42)

    # Feature extraction using TF-IDF
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train = tfidf_vectorizer.fit_transform(train_data['cv'])

    # Create labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_data['applied_job__title'])

    # Debug information
    print("Number of unique categories in training data:", len(label_encoder.classes_))

    # Train a RandomForestClassifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    return rf_classifier, tfidf_vectorizer, label_encoder

# Function to rank resumes based on a job description
def rank_resumes(job_description, rf_classifier, tfidf_vectorizer, label_encoder, applicants):
    job_description = preprocess_text(job_description)

    # Extracting resume text from the 'cv' field of the Applicant model
    applicant_resumes = [preprocess_text(open(applicant.cv.path).read()) for applicant in applicants]

    # Filter out empty applicant resumes
    applicant_resumes = [res for res in applicant_resumes if res.strip() != ""]

    # Feature extraction using TF-IDF for job description and applicant resumes
    job_description_tfidf = tfidf_vectorizer.transform([job_description])
    applicant_resumes_tfidf = tfidf_vectorizer.transform(applicant_resumes)

    # Make predictions for ranking
    ranking_scores = rf_classifier.predict_proba(applicant_resumes_tfidf)

    # Extract the probability of being in class 1 for binary classification
    if ranking_scores.shape[1] == 2:
        ranking_scores = ranking_scores[:, 1]
    else:
        # For multiclass classification, use the max probability across all classes
        ranking_scores = ranking_scores.max(axis=1)

    # Update ranking scores in the Applicant model
    for applicant, ranking_score in zip(applicants, ranking_scores):
        print(f"Applicant: {applicant.name}, Ranking Score: {ranking_score}")
        applicant.ranking_score = ranking_score
        applicant.save()

    # Handle cases where some applicants may not have a corresponding ranking score
    for applicant in applicants:
        if applicant.ranking_score is None:
            # Set a default value for applicants without a ranking score
            applicant.ranking_score = 0.0
            applicant.save()

    return ranking_scores