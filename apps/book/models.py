# django
from django.db import models
from django.db.models.signals import post_save
# third
from datetime import timedelta
# own
from apps.user.models import User

# Create your models here.

class Author(models.Model):
    nameAuthor = models.CharField(max_length=150, blank=False, null=False)
    lastNameAuthor = models.CharField(max_length=150, blank=False, null=False)
    nationalityAuthor = models.CharField(max_length=100, blank=False, null=False)
    descriptionAuthor = models.TextField(blank=False, null=False)
    imageAuthor = models.ImageField(upload_to='book/authors/images/', max_length=255, null=True, blank=True)
    createDateAuthor = models.DateTimeField(auto_now_add=True)
    updateDateAuthor = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """You can add validations here.
        """
        pass

    def save(self, *args, **kwargs):
        """[You can add validations here.]
        """
        super(Author, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['nameAuthor']

    def natural_key(self):
        return f'{self.nameAuthor} {self.lastNameAuthor}'

    def __str__(self):
        return self.nameAuthor

class Book(models.Model):
    titleBook = models.CharField(max_length=150, blank=False, null=False)
    publicationDateBook = models.DateField(blank=False, null=False)
    authorId = models.ManyToManyField(Author)
    descriptionBook = models.TextField(null=True, blank=True)
    amountBook = models.SmallIntegerField(default=1)
    imageBook = models.ImageField(upload_to='book/books/images/', max_length=255, null=True, blank=True)
    createDateBook = models.DateTimeField(auto_now_add=True)
    updateDateBook = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['titleBook']

    def natural_key(self):
        return self.titleBook

    def __str__(self):
        return self.titleBook

    def get_authorId(self):
        return ", ".join([str(c) for c in self.authorId.all()])

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_days = models.SmallIntegerField(default=7)
    status = models.BooleanField(default=True)
    createDate = models.DateTimeField(auto_now_add=True)
    expirationDate = models.DateTimeField(null=True, blank=True)
    updateDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['book']

    def __str__(self):
        return f'{self.book}'

def reduce_book_amount(sender, instance, **kwargs):
    book = instance.book
    if (book.amountBook > 0):
        book.amountBook -= 1
        book.save()

def add_expired_date_reservation(sender, instance, **kwrags):
    book = instance.book
    if (instance.expirationDate is None):
        instance.expirationDate = instance.createDate + timedelta(days=instance.amount_days)
        instance.save()
        book.amountBook += 1
        book.save()

post_save.connect(reduce_book_amount, sender=Reservation)
post_save.connect(add_expired_date_reservation, sender=Reservation)