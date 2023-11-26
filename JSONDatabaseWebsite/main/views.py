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


# Create your views here.

database = JSONDatabase("main/JSON")

def index(request):
    return render(request, "main/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        result = database.find_and({"username":[username], 'password':[password]}, 'accounts')
        if result:
            request.session['is_authenticated'] = True
            request.session['user'] = username
            return redirect("index")
    return render(request, "main/login.html")

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
    return render(request, "main/register.html")

@login_required
def user_view(request):
    if request.method == "POST":
        # Get the search option the user choose
        option_value = request.POST.get('search-option')

        # Get the search filter the user provided and try to evaluate it as a python object
        search_filter = request.POST.get('search-filter')
        try:
            search_filter = ast.literal_eval(search_filter)
        except Exception:
            pass

        # Select a search function based on the option value or return all positions if "all"
        if option_value == 'all':
            return render(request, "main/user_view.html", {"search_filter":search_filter, 
                                                           "search_option":option_value,
                                                           "user_items":[item.items() for item in database.get(request.session['user'])]})
        elif option_value == 'or':
            search_func = database.find_or
        elif option_value == 'and':
            search_func = database.find_and
        else:
            search_func = database.find_key
        
        # If the search succeeded render the items if not render the page without them
        user_items = []
        if search_func(search_filter, request.session['user']):
            user_items = [item.items() for item in search_func(search_filter, request.session['user'])]
        return render(request, "main/user_view.html", {"search_filter":search_filter, 
                                                       "search_option":option_value,
                                                       "user_items":user_items})

    # Get all items from the database and render them
    user_items = [item.items() for item in database.get(request.session['user'])]
    return render(request, "main/user_view.html", {"search_option":'all', "user_items":user_items})

@login_required
def user_view_create(request):
    if request.method == "POST":
        dictionary = {key : value for key, value in zip(request.POST.getlist('key'), request.POST.getlist('value')) if key.strip() != ""}
        database.add_document(dictionary, request.session['user'])
    return render(request, "main/user_view_create.html")