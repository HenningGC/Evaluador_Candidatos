from datetime import datetime

from datetime import datetime



def calculate_ats_score(job_list):

    def calculate_experience(duration):
        start_date_str, end_date_str = duration.split(" / ")
        start_month_name, start_year = start_date_str.split()
        end_month_name, end_year = end_date_str.split()

        spanish_months = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        start_month = spanish_months[start_month_name]
        end_month = spanish_months[end_month_name]

        start_date = datetime(int(start_year), start_month, 1)
        
        if end_date_str.lower() == 'presente':
            end_date = datetime.now()
        else:
            end_date = datetime(int(end_year), end_month, 1)
        
        months_experience = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        return max(0, months_experience)
    
    MAX_JOB_DURATION = 120 
    MAX_RELEVANT_JOBS = 5 
    
    total_experience_months = 0
    relevant_jobs_count = 0
    
    for job in job_list:
        experience = calculate_experience(job['duration'])
        total_experience_months += experience
        relevant_jobs_count += 1
        
    normalized_job_count = min(relevant_jobs_count, MAX_RELEVANT_JOBS)
    job_count_score = (normalized_job_count / MAX_RELEVANT_JOBS) * 40 
    
    normalized_experience = min(total_experience_months, MAX_JOB_DURATION)
    experience_score = (normalized_experience / MAX_JOB_DURATION) * 60 
    
    ats_score = round(job_count_score + experience_score)
    return str(ats_score)
