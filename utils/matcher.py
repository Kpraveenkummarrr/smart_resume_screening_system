from sklearn.metrics.pairwise import cosine_similarity

def calculate_score(resume_vec, job_vec):
    return round(cosine_similarity(resume_vec, job_vec)[0][0] * 100, 2)
