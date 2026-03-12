# engine.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# A dictionary of common tech keywords to look for
TECH_KEYWORDS = [
    "Python", "SQL", "Java", "Machine Learning", "NLP", "Deep Learning", 
    "AWS", "Azure", "Docker", "Kubernetes", "Tableau", "PowerBI", 
    "Scikit-Learn", "TensorFlow", "PyTorch", "Git", "Pandas", "XGBoost", "React"
]

def calculate_similarity(resume_text, job_desc):
    embeddings = model.encode([resume_text, job_desc])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score) * 100, 2)

def analyze_keywords(resume_text, job_desc):
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()
    
    found = []
    missing = []
    
    for skill in TECH_KEYWORDS:
        if skill.lower() in job_desc:
            if skill.lower() in resume_text:
                found.append(skill)
            else:
                missing.append(skill)
                
    return found, missing