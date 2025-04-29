# django
from django import forms
from django.core.exceptions import ValidationError
# third
# own
from apps.book.models import Author, Book, Reservation

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
                'name',
                'lastname',
                'nationality',
                'description',
                'image'
        ]
        labels = {
                'name': 'Author Name',
                'lastname': 'Author Last Name',
                'nationality': 'Author Nacionality',
                'description': 'Author Description',
                'image': 'Author Image'
        }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Name'
                }
            ),
            'lastname': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Last Name'
                }
            ),
            'nationality': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Nationality'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Description'
                }
            )
        }

class BookForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['author_id'].queryset = Author.objects.filter(is_active=True) # para los casos de eliminación logica.

    class Meta:
        model = Book
        fields = [
                'title',
                'publication_date',
                'author_id',
                'description',
                'amount',
                'image'
        ]
        labels = {
            'title': 'Book Title',
            'publication_date': 'Date of Publication of the Book',
            'author_id': 'Authors',
            'description': 'Book Description',
            'amount': 'Amount of Books',
            'image': 'Book Image'
        }
        widgets = {
            'title': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Book Title'
                }
            ),
            'publication_date': forms.SelectDateWidget(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'author_id': forms.SelectMultiple(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Book Description'
                }
            ),
            'amount': forms.NumberInput(
                attrs = {
                    'class': 'form-control'
                }
            )
        }

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Reservation
        fields = '__all__'

    def clean_book(self):
        book = self.cleaned_data['book']
        if (book.amount < 1):
            raise ValidationError('You cannot reservation this book, should exist available units.')
        return book