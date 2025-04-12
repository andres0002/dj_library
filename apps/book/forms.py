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
                'nameAuthor',
                'lastNameAuthor',
                'nationalityAuthor',
                'descriptionAuthor',
                'imageAuthor'
        ]
        labels = {
                'nameAuthor': 'Author Name',
                'lastNameAuthor': 'Author Last Name',
                'nationalityAuthor': 'Author Nacionality',
                'descriptionAuthor': 'Author Description',
                'imageAuthor': 'Author Image'
        }
        widgets = {
            'nameAuthor': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Name'
                }
            ),
            'lastNameAuthor': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Last Name'
                }
            ),
            'nationalityAuthor': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Nationality'
                }
            ),
            'descriptionAuthor': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Author Description'
                }
            )
        }

class BookForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['authorId'].queryset = Author.objects.filter(statusAuthor=True)
    class Meta:
        model = Book
        fields = [
                'titleBook',
                'publicationDateBook',
                'authorId',
                'descriptionBook',
                'amountBook',
                'imageBook'
        ]
        labels = {
            'titleBook': 'Book Title',
            'publicationDateBook': 'Date of Publication of the Book',
            'authorId': 'Authors',
            'descriptionBook': 'Book Description',
            'amountBook': 'Amount of Books',
            'imageBook': 'Book Image'
        }
        widgets = {
            'titleBook': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Book Title'
                }
            ),
            'publicationDateBook': forms.SelectDateWidget(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'authorId': forms.SelectMultiple(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'descriptionBook': forms.Textarea(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Add Book Description'
                }
            ),
            'amountBook': forms.NumberInput(
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
        if (book.amountBook < 1):
            raise ValidationError('You cannot reservation this book, should exist available units.')
        return book