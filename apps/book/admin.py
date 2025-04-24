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
    search_fields = ('name', 'lastname', 'description')
    readonly_fields = ('create_date', 'update_date')
    list_display = ['name', 'lastname',
                    'nationality', 'description',
                    'create_date', 'update_date'
                    ]
    list_filter = ('nationality',)
    resource_class = AuthorResource

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('title',)
    readonly_fields = ('create_date', 'update_date')
    list_display = ['title', 'publication_date',
                    'get_author_id', 'create_date',
                    'update_date'
                    ]
    list_filter = ('publication_date',)
    resource_class = BookResource

class ReservationResource(resources.ModelResource):
    class Meta:
        model = Reservation

class ReservationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ReservationForm
    search_fields = ('book', 'user')
    readonly_fields = ('create_date', 'expiration_date', 'update_date')
    list_filter = ('book', 'user', 'status', 'create_date', 'expiration_date', 'update_date')
    list_display = [
        'book', 'user', 'amount_days', 'status', 'create_date', 'expiration_date', 'update_date'
    ]
    resource_class = ReservationResource

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reservation, ReservationAdmin)