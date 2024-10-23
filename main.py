from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = (
    "Eres un evaluador de candidatos. Vas a recibir el nombre de una oferta de trabajo y el CV del candidato."
    "Vas a puntuar la experiencia de esa persona con un valor numérico entre 0 a 100 según la experiencia.\n"
    "Devolverás solamente un JSON que contenga las llaves: Puntuaje Total, Listado de Experiencia, Descripción de experiencia"
    "El cálculo del puntuaje quiero que sea el mismo que se suele usar en los sistemas de ATS."
    "Además solo puedes tener en cuenta los puestos de trabajo muy relacionados con el del título aportado a la hora de dar un puntuaje por encima de 0.\n"
    "En el listado de experiencia solo puedes mencionar esos trabajos puntuados por encima de 0\n"
    "La descripción de experiencia debe devolver un texto explicativo sobre la experiencia del candidato y porqué ha obtenido la puntuación dada."
    "Finalmente quiero que me devuelvas toda esta información en formato JSON.\n"
    "Ejemplo:\n"
    "{Puntuaje total: 80,\nListado de experiencia: [{Puesto: 'Cajero', Empresa: 'Bar Inc', Duración: '5 años'},{Puesto: 'Cajero', Empresa: 'Testers Supermarkets', Duración: '1 año'}], Descripción de experiencia: '...'}"
)

def evaluate_cv(cv_text, job_title):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Título Oferta: {job_title}\n CV:\n {cv_text}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        print(response)

        return response.choices[0].message.content
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
