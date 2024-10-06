from django.shortcuts import render
from django.http import HttpResponse
from .forms import PromptForm
from openai import OpenAI
import os
from .structured_output_schema import StructuredOutputSchema
import logging 

logger = logging.getLogger('myapp.custom')


def submit_prompt(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            client = OpenAI()

            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system", "content": "Create a quiz."},
                    {"role":"user", "content": prompt}
                ],
                response_format= StructuredOutputSchema
            )
            response = completion.choices[0].message.parsed
            print(response)
            return HttpResponse("Quiz Created")
    else:
        form = PromptForm()

    return render(request, 'submit_prompt.html', {'form': form})
