from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

#OPEN AI
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')
def custom_password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "accounts/password_reset.html", {"error": "Username not found."})

        # Check if passwords match
        if new_password != confirm_password:
            return render(request, "accounts/password_reset.html", {"error": "Passwords do not match."})

        # Set new password
        user.password = make_password(new_password)
        user.save()

        return redirect("password_reset_done")  # Redirect to success page

    return render(request, "accounts/password_reset.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

#OPEN AI
@csrf_exempt
def get_financial_advice(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_input = body.get('message', '')

        prompt = f"Give financial advice based on this input: {user_input}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful financial advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            advice = response['choices'][0]['message']['content']
            return JsonResponse({'advice': advice})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)