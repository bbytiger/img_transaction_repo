from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# these are the authentication related endpoints

def create_user(request):
  if request.method == "POST":
    try:
      print(request)
      username = request.POST['username']
      password = request.POST['password']
      email = request.POST['email']
      first = request.POST['first']
      last = request.POST['last']
      new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first, last_name=last)
      login(request, user)
      return redirect("user_dashboard")

    except Exception as e:
      messages.error(request, e)
      return redirect("signup_user")

  return render(request, "html/register.html")

def delete_user(request):
  logout(request)
  return render(request, "html/delete_account.html")

def login_user(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect("user_dashboard")
    else:
      messages.error(request, "no match found for username and password")
      return redirect("login_user")

  return render(request, "html/login.html")

def logout_user(request):
  logout(request)
  return render(request, "html/logout.html")

# these are the user in-app specific actions

@login_required(login_url="/")
def dashboard(request):
  return render(request, "html/dashboard.html")

def issue_API_key():
  pass

