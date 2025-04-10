from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

import google.generativeai as genai
import json

genai.configure(api_key=settings.GEMINI_API_KEY)


# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})

def dashboard(request):
    template_data = {}
    template_data['title'] = 'Dashboard'
    return render(request, 'home/dashboard.html',
                  {'template_data': template_data})

@csrf_exempt
def api_button_action(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')

            if not question:
                return JsonResponse({'error': 'No question provided'}, status=400)

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"

            headers = {
                "Content-Type": "application/json"
            }

            body = {
                "contents": [{
                    "parts": [{"text": question}]
                }]
            }

            response = requests.post(url, headers=headers, json=body)
            result = response.json()

            # Handle API error
            if response.status_code != 200 or 'candidates' not in result:
                return JsonResponse({'error': result.get('error', 'Unknown error')}, status=500)

            message = result['candidates'][0]['content']['parts'][0]['text']
            return JsonResponse({'message': message})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)