import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from .models import Job, Resume

# Download NLTK stopwords
nltk.download('stopwords')

def load_data(job_id=None):
    jobs = Job.objects.all()
    resumes = Resume.objects.all()

    if not jobs.exists() or not resumes.exists():
        return pd.DataFrame()

    job_df = pd.DataFrame(list(jobs.values()))
    resume_df = pd.DataFrame(list(resumes.values()))

    if job_id is not None:
        resume_df = resume_df[resume_df['applied_job_id'] == job_id]

    df = pd.merge(resume_df, job_df, left_on='applied_job_id', right_on='id', suffixes=('_resume', '_job'))

    df['skills'] = df['skills'].fillna("Unknown")
    df['education'] = df['education'].fillna("Unknown")
    df['work_experience'] = df['work_experience'].fillna("Unknown")

    return df

def create_overall_infos_column(df):
    overall_infos = df.apply(lambda row: f"{row['full_name']} {row['skills']} {row['education']} {row['work_experience']}", axis=1)
    df['overall_infos'] = overall_infos
    return df

from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from .models import Job, Resume
from transformers import BertTokenizer, BertModel


# Load pre-trained model
model = BertModel.from_pretrained('bert-base-uncased')

# Load pre-trained model tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Rest of your code goes here

def text_preprocessing(column):
    if not column.empty:
        column = column.str.lower()
        column = column.str.replace('http\S+|www.\S+|@|%|:|,', '', regex=True)
        stop = stopwords.words('english')
        keywords = column.apply(lambda x: [word for word in x.split() if word not in stop])

        # Define a function to get embeddings
        # Define a function to get embeddings
        def get_bert_embedding(text):
            inputs = tokenizer(text, return_tensors='pt')
            outputs = model(**inputs)

            # Use the representation from the first transformer of the BERT model
            embeddings = outputs.last_hidden_state.detach().numpy()

            # Average the embeddings over sequence length dimension
            document_vector = np.mean(embeddings, axis=1)[0]

            return document_vector

        converted_matrix = column.apply(get_bert_embedding)
        return converted_matrix
    else:
        return None

# Rest of your code goes here

def calculate_cosine_similarity_matrix(cleaned_infos):
    if cleaned_infos is not None:
        # Convert the 1D array of BERT embeddings to a 2D numpy array
        cleaned_infos_array = np.stack(cleaned_infos.values)

        # Calculate cosine similarity
        cosine_similarity_matrix = cosine_similarity(cleaned_infos_array)
        
        return cosine_similarity_matrix
    else:
        return None


# def rank_candidates(similarity_matrix, df, num_top_candidates=5):
#     top_candidates = []
#     included_candidates = set() 

#     for i in range(similarity_matrix.shape[0]):
#         candidates_with_scores = list(enumerate(similarity_matrix[i]))
#         candidates_with_scores.sort(key=lambda x: x[1], reverse=True)

#         for candidate in candidates_with_scores:
#             candidate_index = candidate[0]
#             candidate_name = df.loc[candidate_index, 'full_name']
#             candidate_email = df.loc[candidate_index, 'email']  # Add email retrieval
#             if candidate_name not in included_candidates and len(top_candidates) < num_top_candidates:
#                 top_candidates.append((candidate_name, candidate_email, candidate[1]))
#                 included_candidates.add(candidate_name)

#     # Return the top candidates including email
#     return top_candidates[:num_top_candidates]
def rank_candidates(similarity_matrix, df, num_top_candidates=5):
    top_candidates = []
    included_candidates = set() 

    for i in range(similarity_matrix.shape[0]):
        candidates_with_scores = list(enumerate(similarity_matrix[i]))
        candidates_with_scores.sort(key=lambda x: x[1], reverse=True)

        for candidate in candidates_with_scores:
            candidate_index = candidate[0]
            candidate_name = df.loc[candidate_index, 'full_name']
            candidate_email = df.loc[candidate_index, 'email']  # Add email retrieval
            if candidate_name not in included_candidates and len(top_candidates) < num_top_candidates:
                # Convert score to percentage format
                score_percentage = round(candidate[1] * 100, 2)
                top_candidates.append((candidate_name, candidate_email, score_percentage))
                included_candidates.add(candidate_name)

    # Return the top candidates including email
    return top_candidates[:num_top_candidates]


# 
def apply_text_preprocessing(df):
    cleaned_infos = df['overall_infos'].apply(text_preprocessing)
    return cleaned_infos
