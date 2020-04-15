from django.shortcuts import render, reverse, HttpResponseRedirect
from .models import Author, Recipe
from .forms import AddAuthor, AddRecipe

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

def add_author_view(request):
    html = "addauthorform.html"
    
    if request.method == "POST":
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = Author.objects.create(name=data['name'], bio=data['bio'])
            return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthor()
    
    return render(request, html, {'form': form})

def add_recipe_view(request):
    html = "addrecipeform.html"
    
    if request.method == "POST":
        form = AddRecipe(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            r = Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse("homepage"))
        
    form = AddRecipe()
    
    return render(request, html, {'form': form})
