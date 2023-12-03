from .JSONDatabase import JSONDatabase
from django.shortcuts import redirect
from django.shortcuts import render
from functools import wraps
import ast

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if 'is_authenticated' flag is in the session
        if 'is_authenticated' not in request.session or not request.session['is_authenticated']:
            # Redirect to login view if not authenticated
            return redirect('login')  # Replace 'login' with your actual login URL name or path
        # If authenticated, execute the view function
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_logged_in(request):
    if 'is_authenticated' in request.session:
        return True
    return False

# Create your views here.

database = JSONDatabase("main/JSON")

def index(request):
    return render(request, "main/index.html", {"logged":is_logged_in(request)})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        result = database.find_and({"username":[username], 'password':[password]}, 'accounts')
        if result:
            request.session['is_authenticated'] = True
            request.session['user'] = username
            return redirect("index")
    return render(request, "main/login.html", {"logged":is_logged_in(request)})

@login_required
def logout(request):
    del request.session['is_authenticated']
    del request.session['user']
    return redirect('login')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and email and password and database.find_or({'username':[username]}, 'accounts') == []:
            database.add_document({
                'username':username,
                'email':email,
                'password':password,
            }, 'accounts')
            database.add_category(username)
            return redirect("index")
    return render(request, "main/register.html", {"logged":is_logged_in(request)})

@login_required
def user_view(request):
    if request.method == "POST":
        search_filter = request.POST.get('search-filter')
        if search_filter == "":
            return render(request, 'main/user_view.html', {'user_items':database.get(request.session['user']),
                                                           'search_filter':search_filter})

        return render(request, 'main/user_view.html', {"user_items":database.find_or({"Title":[search_filter]}, request.session['user']),
                                                       'search_filter':search_filter})

    user_items = database.get(request.session['user'])
    return render(request, 'main/user_view.html', {"logged":is_logged_in(request), 'user_items':user_items, 'search_filter':""})



@login_required
def user_view_create(request):
    if request.method == "POST":
        dictionary = {"Title": request.POST.get("title"),
                      "Content": request.POST.get("content")}
        if dictionary["Title"].strip() != "":
            database.add_document(dictionary, request.session['user'])
    return render(request, "main/user_view_create.html", {"logged":is_logged_in(request)})


@login_required
def user_view_delete(request, id):
    document = database.find_or({"uuid":[id]}, request.session['user'], True)
    if document:
        database.remove_document(document[0], request.session['user'])
    return redirect('user_view')