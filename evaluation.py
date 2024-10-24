from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime
from constants import *
from helpers import *
import os
import instructor
import json

__all__ = ['evaluate_cv', 'agentic_evaluate_cv']

load_dotenv()

defaultClient = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

class Job(BaseModel):
    puesto: str
    empresa: str
    duracion: str

class JobList(BaseModel):
    ListadoExperiencia: list[Job]

class CompleteJobEvent(BaseModel):
    PuntuajeTotal: int
    Experiencias: JobList
    DescripcionExperiencia: str


def evaluate_cv(cv_text, job_title):

    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": f"Título Oferta: {job_title}\n CV:\n {cv_text}"}
    ]

    try:
        completion = defaultClient.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format=CompleteJobEvent,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def agentic_evaluate_cv(cv_text, job_title):
    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": f"Título Oferta: {job_title}\n CV:\n {cv_text}"}
    ]
    client = instructor.from_openai(OpenAI(api_key= os.getenv("OPENAI_API_KEY")))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_model=JobList,
    )

    response_message = completion.ListadoExperiencia

    messages.append({"role": "system", "content": str(response_message)})

    messages.append({"role": "user", "content": "Now that you have the list of relevant jobs, I want you to calculate the score using the calculate_ats_function"})

    completion = defaultClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[tool_calculate_ats_score],
        tool_choice="required"
    )

    response_message = completion.choices[0].message

    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "calculate_ats_score": calculate_ats_score
        }

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                job_list=json.loads(function_args.get("job_list")),
            )
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format=CompleteJobEvent
        )
        return completion.choices[0].message.content
    