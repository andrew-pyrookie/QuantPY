from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from .models import Users
from django.http import JsonResponse
import json

def home(request):
    return render(request, "home.html")

# views.py
def login_view(request):
    if request.method == "POST":
        # Check if the request is JSON (for API login)
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                email = data.get("email")
                password = data.get("password")
                next_url = data.get('next', '/dashboard/')  # Get next parameter or default
                
                user = Users.objects.filter(corporate_email=email).first()
                if user and user.check_password(password):
                    request.session["user_id"] = user.id  # Session-based login
                    return JsonResponse({"redirect": next_url, "message": "Login successful!"})
                return JsonResponse({"error": "Invalid credentials"}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid request format"}, status=400)

        # Handle form-based login
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Users.objects.get(corporate_email=email)
            if user.check_password(password):
                login(request, user)
                return redirect("dashboard")  # Redirect to dashboard
            else:
                messages.error(request, "Invalid credentials.")
        except Users.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, "login.html")

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# views.py
def signup_view(request):
    if request.method == "POST":
        # Extract all required fields from POST data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        company_name = request.POST.get("company_name")
        corporate_email = request.POST.get("email")
        password = request.POST.get("password")
        company_type = request.POST.get("company_type")  # Add these fields in your template
        industry = request.POST.get("industry")          # Add these fields in your template

        if Users.objects.filter(corporate_email=corporate_email).exists():
            messages.error(request, "Email already exists.")
        else:
            # Create user with all required fields
            user = Users.objects.create(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                company_type=company_type,
                industry=industry,
                corporate_email=corporate_email,
                # Initially set a placeholder; will be replaced
                password_hash=''  
            )
            user.set_password(password)  # Hashes password and saves
            request.session['user_id'] = user.id
            return redirect('dashboard')  # Ensure 'dashboard' URL exists
    return render(request, "signup.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")