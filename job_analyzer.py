import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_job(job_description, resume_text):
    prompt = f"""
You are an expert enterprise recruiter hiring for senior roles such as:

- Salesforce Program Manager
- SAP Delivery Manager
- Enterprise Transformation Leader

Analyze the job description against the candidate resume.

Candidate Resume:
{resume_text}

Job Description:
{job_description}

Your tasks:

1. Extract:
   - role
   - required_skills (list)
   - experience_required
   - domain

2. Evaluate candidate fit:
   - match_score (0–100)
   - matching_experience (list based ONLY on resume)
   - gaps (list based ONLY on resume)

3. Suggest positioning strategy (list)

4. Resume suggestions (list)

5. Final recommendation:
   - decision: Apply / Apply with Changes / Skip
   - reason

IMPORTANT:
- Use ONLY the resume provided (no assumptions)
- Be realistic like a recruiter
- Keep answers concise
- Return ONLY valid JSON
- Do NOT include markdown (no ```)

Format:

{{
  "role": "...",
  "required_skills": ["...", "..."],
  "experience_required": "...",
  "domain": "...",
  "match_score": 0,
  "matching_experience": ["...", "..."],
  "gaps": ["...", "..."],
  "positioning_strategy": ["...", "..."],
  "resume_suggestions": ["...", "..."],
  "decision": "...",
  "reason": "..."
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content