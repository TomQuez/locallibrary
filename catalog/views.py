from django.shortcuts import render
from django.views import generic
# Create your views here.
from catalog.models import Book,Author,BookInstance,Genre

def index(request):
    """View function for home page of site."""
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.all().count()
    num_genre=Genre.objects.all().count()
    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
    }
    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model=Book
    paginate_by=2
   
    
class BookDetailView(generic.DetailView):
    model=Book
    
class AuthorListView(generic.ListView):
    model=Author
    paginate_by=2
    
class AuthorDetailView(generic.DetailView):
    model=Author
    