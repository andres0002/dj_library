# django
from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# third
# own
from apps.book.models import Author, Book, Reservation
from apps.book.forms import ReservationForm
from apps.book.actions import elimination_from_actions_py_Authors_by_filter

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
    actions = (
        elimination_from_actions_py_Authors_by_filter, # define in actions.py
        'elimination_from_class_model_admin_Authors_by_filter', # define in class model_admin
        'elimination_logical_from_class_model_admin_Authors' # define in class model_admin
    )

    # Definir action.
    def elimination_from_class_model_admin_Authors_by_filter(self, request, queryset): # actions en admin.
        if not request.user.has_perm(('app.can_mark_as_read',)): # permissions
            messages.error(request, "No tienes permiso para marcar como leído.")
            return
        # queryset = queryset.exclude(name__icontains='author') # i -> indistinto de mayúsculas y minúsculas, contains -> que contengo lo indicado.
        # for author in queryset:
        #     author.delete()
        # puedes mostrar un mensaje al usuario -> otra forma.
        self.message_user(request, "Authors successfully removed -> message_user.")
        # puedes mostrar un mensaje al usuario -> types.
        messages.success(request, "Authors successfully removed.")
        messages.error(request, "Authors errorfully removed.")
        messages.warning(request, "Authors warningfully removed.")
        messages.info(request, "Authors infofully removed.")
    
    # Definir action.
    def elimination_logical_from_class_model_admin_Authors(self, request, queryset): # actions en admin.
        if not request.user.has_perm(('app.can_mark_as_read',)): # permissions
            messages.error(request, "No tienes permiso para marcar como leído.")
            return
        # for author in queryset:
        #     author.is_active = False
        #     author.save()
        # puedes mostrar un mensaje al usuario -> otra forma.
        self.message_user(request, "Authors successfully removed -> message_user.")
        # puedes mostrar un mensaje al usuario -> types.
        messages.success(request, "Authors successfully removed.")
        messages.error(request, "Authors errorfully removed.")
        messages.warning(request, "Authors warningfully removed.")
        messages.info(request, "Authors infofully removed.")
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        # 'delete_selected' -> este action lo trae por default django.
        # if 'delete_selected' in actions: # para eliminar actions especificas.
        #     del actions['delete_selected'] # elimina el action.
        # if 'elimination_from_actions_py_Authors_by_filter' in actions: # para eliminar actions especificas.
        #     del actions['elimination_from_actions_py_Authors_by_filter'] # elimina el action.
        # if 'elimination_from_class_model_admin_Authors_by_filter' in actions: # para eliminar actions especificas.
        #     del actions['elimination_from_class_model_admin_Authors_by_filter'] # elimina el action.
        return actions

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('title',)
    readonly_fields = ('create_date', 'update_date')
    list_display = ['title', 'publication_date',
                    'get_authors', 'create_date',
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