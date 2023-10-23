from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    """Cet objet représente une catégorie ou un genre littéraire"""
    name=models.CharField(max_length=200,help_text="Enter a book genre (e.g. Science Fiction)")
    
    def __str__(self):
        """cette méthode surcharge __str__ et est obligatoirement requise par django. Elle retounre une chaine de caractère pour identifier l'instance de la classe d'objet"""
        return self.name
    
class Language(models.Model):
    """Model representing a language(e.g. English, French, Japanese,etc)."""
    name=models.CharField(max_length=200,help_text="Enter the book's natural language(e.e. Englis, Franch, Japanese,etc...)")
    def __str__(self):
        """string for representing the Model object(in admin site)"""
        return self.name


class Book(models.Model):
    """cet objet représente un livre (mais ne traite pas les copies disponible en rayon pour le prêt)"""
    title=models.CharField(max_length=200)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    summary=models.TextField(max_length=1000,help_text='Enter a brief description of the book')
    isbn=models.CharField('ISBN',max_length=13,help_text='13 Characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre=models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language=models.ForeignKey(Language,on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering=['title','author']
    
    def display_genre(self):
        """Creates a string for the Genre.this is required to display genre in Admin."""
        return ','.join([genre.name for genre in self.genre.all()[:3]])
    
    display_genre.short_description='Genre'
    
    def __str__(self):
        """fonction requise par django pour manipuler les objets Book dans la base de données."""
        return self.title
    
    
    def get_absolute_url(self):
        """Cette fonction est requise par django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse('book-detail',args=[str(self.id)])
    
class BookInstance(models.Model):
    """Cet objet permet de modéliser les copies d'un ouvrage (i.e. qui peut être emprunté physiquement)."""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book=models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )
    status=models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text='Book Availability')
    class Meta:
        ordering=['due_back']
    
    def __str__(self):
        """Fonction requise par django pour manipuler les objets Book dans la base de données."""
        return f'{self.id}({self.book.title})'
    
class Author(models.Model):
    """Model représentant un Auteur"""
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField('Died',null=True,blank=True)
    
    class Meta:
        ordering=['last_name','first_name']
        
    def get_absolute_url(self):
        """Return the url to access a particular author instance."""
        return reverse('author-detail',args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.last_name},{self.first_name}'