from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

class Job(BaseModel):
    puesto: str
    empresa: str
    duracion: str

class JobEvent(BaseModel):
    PuntuajeTotal: int
    ListadoExperiencia: list[Job]
    DescripcionExperiencia: str

SYSTEM_PROMPT = (

    """
    You are a CV & Resume - Evaluator (ATS)
    Evaluate a candidate's CV against a specified job offer title.
    Review the candidate's CV and identify any relevant experience directly related to the specified job offer title. Score the candidate's experience from 0 to 100 based on the relevance and quality of the related job experiences.

    # Steps

    1. **Identify Relevant Experience**: Analyze the candidate’s CV and extract job experiences where the role matches or aligns closely with the specified job offer title.
    
    2. **Scoring Experience**: Based on relevance and duration, assign a numerical score between 0 and 100. Only consider jobs directly related to the provided job title.

    3. **List of Relevant Experiences**: For each relevant experience, gather:
    - Position
    - Company
    - Duration

    4. **Description Generation**: Write a concise explanation detailing the candidate's relevant experience and justify the score given.

    # Examples

    **Example Input**
    - CV: Candidate has experience as a Cashier at XYZ Market for 2 years and as a Customer Service Representative for 1 year.
    - Job Offer Title: Cashier at Dia Supermarket

    **Example Output**

    "score": 80,
    "relevant_experience_list": [
        {
        "position": "Cashier",
        "company": "XYZ Market",
        "duration": "2 years"
        }
    ],
    "experience_description": "The candidate received a score of 80 due to their 2 years of experience as a cashier which directly aligns with the job offer. The role at XYZ Market demonstrates necessary skills for the Cashier role at Dia Supermarket."
    }
    ```

    # Notes

    - Ensure experiences not relevant to the job title, such as delivery roles for a cashier position, are excluded from consideration and the JSON output.
    - Any job experiences must be clearly related to the job title in order to be included and affect the score.
    - Pay attention to detail, ensuring that only relevant experiences are used for scoring and reflection.
    - The answer should be in Spanish
    """
)

def evaluate_cv(cv_text, job_title):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Título Oferta: {job_title}\n CV:\n {cv_text}"}
    ]

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format=JobEvent,
        )

        print(completion)
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    with gr.Blocks() as demo:
        gr.Markdown("""
            # CV Evaluator with GPT
            Enter a candidate's CV and list of related jobs to evaluate their qualifications.
            The AI will provide a total score along with explanations for each evaluation.
        """)
        
        cv_input = gr.Textbox(label="Enter CV (as text)", placeholder="Paste the CV here...", lines=10)
        job_title_input = gr.Textbox(label="Enter Job Title", placeholder="Example: Senior Software Engineer at ACME", lines=2)
        
        evaluate_button = gr.Button("Evaluate CV")
        output_text = gr.Textbox(label="Evaluation Results", lines=10)
        
        evaluate_button.click(fn=evaluate_cv, inputs=[cv_input, job_title_input], outputs=[output_text])

    demo.launch()

if __name__ == "__main__":
    main()
