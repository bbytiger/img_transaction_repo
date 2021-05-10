from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from pprint import pprint # may be useful in the future if need to log requests for analytics

# these are the authentication related endpoints

def create_user(request):
  if request.user.is_authenticated and request.user.is_active:
    return redirect('user_dashboard')

  if request.method == "POST":
    try:
      print(request)
      username = request.POST['username']
      password = request.POST['password']
      email = request.POST['email']
      first = request.POST['first']
      last = request.POST['last']
      if len(User.objects.filter(username=username)) == 0 and len(User.objects.filter(email=email)) == 0:
        new_user = User.objects.create_user(username=username, password=password, email=email, first_name=first, last_name=last)
        login(request, new_user)
        return redirect("user_dashboard")
      else:
        messages.error(request, "user already exists")
        return redirect("signup_user")
    except Exception as e:
      messages.error(request, e)
      return redirect("signup_user")

  return render(request, "html/register.html")

def login_user(request):
  if request.user.is_authenticated and request.user.is_active:
    return redirect('user_dashboard')

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

def perform_logout(request):
  if request.user.is_authenticated and request.user.is_active:
    request.session['from_redirect'] = True
    return HttpResponseRedirect(reverse("logout_user"))
  return redirect("login_user")

def logout_user(request):
  if request.user.is_authenticated and request.user.is_active:
    if 'from_redirect' in request.session.keys():
      logout(request)
      return render(request, "html/logout.html")
  return redirect("login_user")

def delete_user(request):
  logout(request)
  return render(request, "html/delete_account.html")

# these are the user in-app specific actions

@login_required(login_url="/login")
def dashboard(request):
  print(request.session.keys())
  print(request.session.items())
  try:
    my_name = User.objects.filter(username=request.user)[0].first_name
  except:
    my_name = ""
  return render(request, "html/dashboard.html", {'my_name': my_name})

@login_required(login_url="/login")
def issue_API_key():
  pass

@login_required(login_url="/login")
def protected_serve(request, path, document_root=None, show_indexes=False):
  if 'Authorization' not in request.headers:
    # this is the user viewing endpoint
    try:
      url = int(request.path.split('/')[-2].split("user_")[-1])
      k = User.objects.filter(username=request.user)
      if k.count() == 1 and k[0].id == url:
        return serve(request, path, document_root, show_indexes)
      else:
        return redirect("login_user")
    except:
      return redirect("login_user")
  else:
    # this is the API return endpoint
    return Response({"detail":"Authorization credentials were not provided."}, status=401)