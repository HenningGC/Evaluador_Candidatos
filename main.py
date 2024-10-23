from evaluation import evaluate_cv, agentic_evaluate_cv
import gradio as gr

def main():
    with gr.Blocks() as demo:
        with gr.Tab("Function Mode"):
            gr.Markdown("""
                # CV Evaluator with GPT - Function Mode
                In Function Mode, you can interact with the AI as an assistant to help evaluate CVs via function calling.
            """)
            
            cv_input = gr.Textbox(label="Enter CV (as text)", placeholder="Paste the CV here...", lines=10)
            job_title_input = gr.Textbox(label="Enter Job Title", placeholder="Example: Senior Software Engineer at ACME", lines=2)
            
            evaluate_button = gr.Button("Evaluate CV")
            output_text = gr.Textbox(label="Evaluation Results", lines=10)
            evaluate_button.click(fn=agentic_evaluate_cv, inputs=[cv_input, job_title_input], outputs=[output_text])
        with gr.Tab("Default Mode"):
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
