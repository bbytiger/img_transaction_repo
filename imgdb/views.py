from django.shortcuts import render
from django.contrib.auth import User, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# these are the authentication related endpoints

def create_user(request):
  try:
    print(request)
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first = request.POST['first']
    last = request.POST['last']
    new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first, last_name=last)
    login(request, user)
    return redirect("dashboard")
  except Exception as e:
    messages.error(e)
    return redirect("register")

def delete_user(request):
  logout(request)
  return render(request, "delete_account.html")

def login_user(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect("dashboard")
    else:
      messages.error("no match found for username and password")
      return redirect("")
  return render(request, "login.html")

def logout_user(request):
  logout(request)
  return render(request, "logout.html")

# these are the user in-app specific actions

@login_required(login_url="/")
def dashboard(request):
  return render(request, "dashboard.html")

def issue_API_key():
  pass

