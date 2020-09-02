from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Author, Recipe
from .forms import AddAuthor, AddRecipe, LoginForm

def index_view(request):
    recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": recipes})

def author_view(request, id):
    author = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=author)
    return render(request, "author.html", {"recipes": recipes, "author":author})

def recipes_view(request, id):
    recipes = Recipe.objects.get(id=id)
    return render(request, "recipe.html", {"recipes": recipes})

@staff_member_required
def add_author_view(request):
    html = "addauthorform.html"
    
    if request.method == "POST":
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], password=data['password'])
            a = Author.objects.create(name=data['name'], bio=data['bio'], user=user)
            return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthor()
    
    return render(request, html, {'form': form})

@login_required()
def add_recipe_view(request):
    html = "addrecipeform.html"
    
    if request.method == "POST":
        form = AddRecipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse("homepage"))
    else:   
        form = AddRecipe()
    
    return render(request, html, {'form': form})

def register_view(request):
    html = "registerform.html"
    form = NONE
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            login(request, user)
            Author.objects.create(
                name=data['name'],
                user=user
            )
            return HttpResponseRedirect(reverse("homepage"))
    else:
        form = RegisterForm()
    return render(request, html, {'form': form})

def login_view(request):
    html = 'loginform.html'
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            # breakpoint()
            # form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))