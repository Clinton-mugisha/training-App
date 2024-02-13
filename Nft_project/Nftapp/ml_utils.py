import pandas as pd
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

def text_preprocessing(column):
    if not column.empty:
        column = column.str.lower()
        column = column.str.replace('http\S+|www.\S+|@|%|:|,', '', regex=True)
        stop = stopwords.words('english')
        keywords = column.apply(lambda x: [word for word in x.split() if word not in stop])

        CV = CountVectorizer()
        converted_matrix = CV.fit_transform(column)

        print("Converted matrix shape:", converted_matrix.shape)  # Add a print statement to display the shape of the converted matrix

        return converted_matrix
    else:
        return None

def calculate_cosine_similarity_matrix(cleaned_infos):
    if cleaned_infos is not None:
        cleaned_infos = csr_matrix(cleaned_infos)
        cosine_similarity_matrix = cosine_similarity(cleaned_infos)
        return cosine_similarity_matrix
    else:
        return None

def rank_candidates(similarity_matrix, df, num_top_candidates=5):
    top_candidates = []
    included_candidates = set() 

    for i in range(similarity_matrix.shape[0]):
        candidates_with_scores = list(enumerate(similarity_matrix[i]))
        candidates_with_scores.sort(key=lambda x: x[1], reverse=True)

        for candidate in candidates_with_scores:
            candidate_name = df.loc[candidate[0], 'full_name']
            if candidate_name not in included_candidates and len(top_candidates) < num_top_candidates:
                top_candidates.append((candidate_name, candidate[1]))
                included_candidates.add(candidate_name)

    # Display the top candidates with proper formatting
    print("Top 5 Candidates:")
    for idx, (name, score) in enumerate(top_candidates[:5], 1):
        print(f"Rank {idx}:")
        print(f"Name: {name}")
        print(f"Score: {score}")
        print()  # Add an empty line for separation

    return top_candidates[:5]


def apply_text_preprocessing(df):
    cleaned_infos = df['overall_infos'].apply(text_preprocessing)
    return cleaned_infos
