# Import necessary libraries
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from django.views import View
from .models import Job, Applicant
from .forms import JobForm, ApplicantForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import PyPDF2
from docx import Document

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Function to download NLTK resources
def download_nltk_resources():
    nltk.download('stopwords')
    nltk.download('wordnet')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

# Function to extract text from Word document
def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

# Run the utility function for downloading NLTK resources
download_nltk_resources()

class RankResumesView(View):
    template_name = 'rank_resumes.html'

    def get(self, request, *args, **kwargs):
        # Retrieve all applicants and their associated job descriptions from the database
        applicants = Applicant.objects.all()

        # Create a DataFrame from the Django models
        df = pd.DataFrame(list(applicants.values('cv', 'applied_job__description')), columns=['cv', 'description'])

        # Define the preprocess_text function

        def preprocess_text(text):
            if not isinstance(text, str):
                return ""

            print(f"Original Text: {text}")

            # Extract text from PDF and Word documents
            if text.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(text)
                print(f"Extracted Text from PDF: {extracted_text}")
                text = extracted_text
            elif text.endswith('.docx'):
                extracted_text = extract_text_from_word(text)
                print(f"Extracted Text from Word: {extracted_text}")
                text = extracted_text

            print(f"After Extracting Text: {text}")

            # Check if the input is a string
            text = text.lower()
            print(f"After Lowercasing: {text}")

            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            print(f"After Removing Special Characters: {text}")

            # Check the length of the text after removing special characters
            print(f"Text Length After Removing Special Characters: {len(text)}")

            stop_words = set(stopwords.words('english'))
            text = ' '.join(word for word in text.split() if word not in stop_words)
            print(f"After Removing Stopwords: {text}")

            # Check the length of the text after removing stopwords
            print(f"Text Length After Removing Stopwords: {len(text)}")

            return text

        # Apply preprocessing to 'description' column
        df['description'] = df['description'].apply(preprocess_text)

        # Print processed text for debugging
        print("Processed Text:")
        for example in df['description'].head(5):  # Print the first 5 examples
            print(example)

        # Feature extraction using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=500000)
        X_train = tfidf_vectorizer.fit_transform(df['description'])

        # Check if the vocabulary is empty
        if not tfidf_vectorizer.vocabulary_:
            print("TF-IDF Vocabulary is empty. Check your preprocessing and input data.")

        # Create labels
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(df['cv'])

        # Train a RandomForestClassifier
        rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier.fit(X_train, y_train)

        # Make predictions for ranking
        ranking_scores = rf_classifier.predict_proba(tfidf_vectorizer.transform(df['description']))[:, 1]

        # Add ranking scores to the original DataFrame
        df['Ranking_Score'] = ranking_scores

        # Sort the DataFrame based on the ranking scores
        ranked_df = df.sort_values(by='Ranking_Score', ascending=False)

        # Render the template with the ranked data
        return render(request, self.template_name, {'ranked_df': ranked_df[['description', 'Ranking_Score']]})


class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'

class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'

class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_create.html'
    success_url = reverse_lazy('job_list')

class ApplicantCreateView(CreateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicant_create.html'
    success_url = reverse_lazy('job_list')
