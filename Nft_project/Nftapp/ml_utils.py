import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

    df = pd.merge(resume_df, job_df, left_on='applied_job_id', right_on='id', suffixes=('_resume', '_job'))

    df['skills'] = df['skills'].fillna("Unknown")
    df['education'] = df['education'].fillna("Unknown")
    df['work_experience'] = df['work_experience'].fillna("Unknown")

    if job_id is not None:
        # Filter candidates for a specific job
        df = df[df['id_job'] == job_id]

    return df

def create_overall_infos_column(df):
    overall_infos = df.apply(lambda row: f"{row['full_name']} {row['skills']} {row['education']} {row['work_experience']}", axis=1)
    df['overall_infos'] = overall_infos
    print(df)
    return df

def text_preprocessing(column):
    if not column.empty:
        column = column.str.lower()
        column = column.str.replace('http\S+|www.\S+|@|%|:|,', '', case=False)
        word_tokens = column.str.split()
        stop = stopwords.words('english')
        keywords = word_tokens.apply(lambda x: [item for item in x if item not in stop])

        # Add debugging print statements
        print("Word Tokens:", word_tokens)
        print("Keywords:", keywords)

        for i in range(len(keywords)):
            if keywords[i]:  # Check if the list is not empty
                keywords[i] = " ".join(keywords[i])
                print(keywords[i])

        return keywords
    else:
        return column

def apply_text_preprocessing(df):
    if df.empty or 'overall_infos' not in df.columns:
        return pd.Series()

    try:
        df['cleaned_infos'] = text_preprocessing(df['overall_infos'])
    except KeyError as e:
        print(f"Error processing text: {e}")
        return pd.Series()

    return df['cleaned_infos']

def calculate_cosine_similarity_matrix(cleaned_infos):
    CV = CountVectorizer()
    converted_matrix = CV.fit_transform(cleaned_infos)

    cosine_similarity_matrix = cosine_similarity(converted_matrix)
    return cosine_similarity_matrix

def rank_candidates(similarity_matrix, num_top_candidates=5):
    top_candidates = []

    for i in range(similarity_matrix.shape[0]):
        candidates_with_scores = list(enumerate(similarity_matrix[i]))
        candidates_with_scores.sort(key=lambda x: x[1], reverse=True)
        top_candidates_for_job = candidates_with_scores[:num_top_candidates]
        top_candidates.append(top_candidates_for_job)
        print(top_candidates_for_job)

    return top_candidates
