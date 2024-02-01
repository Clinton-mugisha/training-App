# Nftapp/ml_utils.py
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Job, Resume

# Download NLTK stopwords
nltk.download('stopwords')

def load_data():
    jobs = Job.objects.all()
    resumes = Resume.objects.all()

    job_df = pd.DataFrame(list(jobs.values()))
    resume_df = pd.DataFrame(list(resumes.values()))

    df = pd.merge(resume_df, job_df, left_on='applied_job_id', right_on='id', suffixes=('_resume', '_job'))

    df['skills'] = df['skills'].fillna("Unknown")
    df['education'] = df['education'].fillna("Unknown")
    df['work_experience'] = df['work_experience'].fillna("Unknown")

    return df

def create_overall_infos_column(df):
    overall_infos = df.apply(lambda row: f"{row['full_name']} {row['skills']} {row['education']} {row['work_experience']}", axis=1)
    df['overall_infos'] = overall_infos
    print(overall_infos)
    return df

def text_preprocessing(column):
    column = column.str.lower()
    column = column.str.replace('http\S+|www.\S+|@|%|:|,', '', case=False)
    word_tokens = column.str.split()
    stop = stopwords.words('english')
    keywords = word_tokens.apply(lambda x: [item for item in x if item not in stop])
    for i in range(len(keywords)):
        keywords[i] = " ".join(keywords[i])
        print(keywords[i])
    return keywords

def apply_text_preprocessing(df):
    df.loc[:, 'cleaned_infos'] = text_preprocessing(df['overall_infos'])
    return df['cleaned_infos']

def calculate_cosine_similarity_matrix(cleaned_infos):
    CV = CountVectorizer()
    converted_matrix = CV.fit_transform(cleaned_infos)

    cosine_similarity_matrix = cosine_similarity(converted_matrix)
    return cosine_similarity_matrix

def find_job_related_to_skill(df, skill):
    return df[df['skill'].str.contains(skill)]

def rank_candidates(similarity_matrix, num_top_candidates=5):
    top_candidates = []

    for i in range(similarity_matrix.shape[0]):
        candidates_with_scores = list(enumerate(similarity_matrix[i]))
        candidates_with_scores.sort(key=lambda x: x[1], reverse=True)
        top_candidates_for_job = candidates_with_scores[:num_top_candidates]
        top_candidates.append(top_candidates_for_job)

    return top_candidates




