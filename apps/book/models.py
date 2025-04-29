# django
from django.db import models
# third
# own
from apps.user.models import User

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    lastname = models.CharField(max_length=150, blank=False, null=False)
    nationality = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='book/authors/images/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # validations antes de cualquier action.
    def clean(self):
        """You can add validations here.
        """
        pass

    # validations al momento de save.
    def save(self, *args, **kwargs):
        """[You can add validations here.]
        """
        super(Author, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']

    def natural_key(self):
        return f'{self.name} {self.lastname}'

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    publication_date = models.DateField(blank=False, null=False)
    # para que tenga author anonymous debe tener blank=True and null=True, eso para si se quiere implementar.
    # la elimination logical al author.
    author_id = models.ManyToManyField(Author)
    description = models.TextField(null=True, blank=True)
    amount = models.SmallIntegerField(default=1)
    image = models.ImageField(upload_to='book/books/images/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def natural_key(self):
        return self.title

    def __str__(self):
        return self.title

    def get_author_id(self):
        return ", ".join([str(c) for c in self.author_id.all()])

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_days = models.SmallIntegerField(default=7)
    expiration_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['book']

    def __str__(self):
        return f'{self.book}'