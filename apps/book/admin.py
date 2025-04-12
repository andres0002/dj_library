# django
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# third
# own
from apps.book.models import Author, Book, Reservation
from apps.book.forms import ReservationForm

# Register your models here.

class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author
class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('nameAuthor', 'lastNameAuthor', 'descriptionAuthor')
    readonly_fields = ('createDateAuthor', 'updateDateAuthor')
    list_display = ['nameAuthor', 'lastNameAuthor',
                    'nationalityAuthor', 'descriptionAuthor',
                    'createDateAuthor', 'updateDateAuthor'
                    ]
    list_filter = ('nationalityAuthor',)
    resource_class = AuthorResource

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('titleBook',)
    readonly_fields = ('createDateBook', 'updateDateBook')
    list_display = ['titleBook', 'publicationDateBook',
                    'get_authorId', 'createDateBook',
                    'updateDateBook'
                    ]
    list_filter = ('publicationDateBook',)
    resource_class = BookResource

class ReservationResource(resources.ModelResource):
    class Meta:
        model = Reservation

class ReservationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ReservationForm
    search_fields = ('book', 'user')
    readonly_fields = ('createDate', 'expirationDate', 'updateDate')
    list_filter = ('book', 'user', 'status', 'createDate', 'expirationDate', 'updateDate')
    list_display = [
        'book', 'user', 'amount_days', 'status', 'createDate', 'expirationDate', 'updateDate'
    ]
    resource_class = ReservationResource

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reservation, ReservationAdmin)