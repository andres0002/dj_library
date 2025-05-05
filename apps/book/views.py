# py
from time import time
import json
# django
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.db.models import Q
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
# thrid
# own
from apps.book.models import Author, Book, Reservation
from apps.book.forms import AuthorForm, BookForm
from apps.user.mixins import LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin
from apps.base.utils.request_utils import is_ajax

# Create your views here.

#Section of Authors.
class AuthorsList(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, TemplateView):
    permission_required = ('user.view_author', 'user.add_author', 'user.change_author', 'user.delete_author')
    template_name = 'author/authors_table.html'

class AuthorsTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, ListView):
    permission_required = ('user.view_author', 'user.add_author', 'user.change_author', 'user.delete_author')
    model = Author

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('book:authors_list')

class CreateAuthor(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, CreateView):
    permission_required = ('user.add_author',)
    model = Author
    form_class = AuthorForm
    template_name = 'author/create_author.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES)
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} registered.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} register.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:authors_list')

class UpdateAuthor(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, UpdateView):
    permission_required = ('user.change_author',)
    model = Author
    form_class = AuthorForm
    template_name = 'author/update_author.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES, instance=self.get_object())
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} updation.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} updation.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:authors_list')

class DeleteAuthor(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, DeleteView):
    permission_required = ('user.delete_author',)
    model = Author
    template_name = 'author/delete_author.html'

    def delete(self, request, *args, **kwargs):
        if is_ajax(request):
            author = self.get_object()
            # elimination direct.
            author.delete()
            # logical elimination.
            # author.is_active = False
            # author.save()
            message = f'Successfully {self.model.__name__} elimination.'
            error = 'There are no errors.'
            response = JsonResponse({'message':message, 'error':error})
            response.status_code = 204
            return response
        else:
            redirect('book:authors_list')

# Server Side In DataTable
class AuthorsListServerSideInDataTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, TemplateView):
    permission_required = ('user.view_author', 'user.add_author', 'user.change_author', 'user.delete_author')
    template_name = 'author/authors_table_serve_side_in_datatable.html'

class AuthorsTableServerSideInDataTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, ListView):
    permission_required = ('user.view_author', 'user.add_author', 'user.change_author', 'user.delete_author')
    model = Author

    def get_queryset(self):
        search = self.request.GET.get('search','').strip() # obtiene el value del search y quita espacios al start and end del string.
        # , si tiene '-name' al inicio del campo se ordena de forma descendente y si no 'name' de forma ascendente.
        order = self.request.GET.get('order', '').strip() # obtiene la columna por la que se quiere ordenar la table.
        # Reemplazo del campo ficticio "#" por el campo real "id".
        if '#' in order:
            order = order.replace('#', 'id')
        queryset = self.model.objects.filter(is_active=True) # obtiene solo los authors que no se han eliminado de forma logical.
        if search: # aplica filter si search is != ''.
            queryset = queryset.filter( # filtra si cualquier campo coincide.
                Q(name__icontains=search) |
                Q(lastname__icontains=search) |
                Q(description__icontains=search) |
                Q(nationality__icontains=search)
            )
        if order == '':
            queryset = queryset.values( # solo me trae estos campos.
                'id',
                'name',
                'lastname',
                'description',
                'nationality',
                # 'create_date',
                # 'update_date'
            ).distinct()
        else:
            queryset = queryset.values( # solo me trae estos campos.
                'id',
                'name',
                'lastname',
                'description',
                'nationality',
                # 'create_date',
                # 'update_date'
            ).distinct().order_by(order)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            data = self.get_queryset()
            data_list = []
            for index, author in enumerate(data[start:start+limit],start):
                author['#'] = index + 1
                data_list.append(author)
            data = {
                "length": data.count(),
                "objects": data_list
            }
            return HttpResponse(json.dumps(data), 'application/json')
        else:
            return redirect('book:authors_list_serve_side_in_datetable')

class CreateAuthorServerSideInDataTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, CreateView):
    permission_required = ('user.add_author',)
    model = Author
    form_class = AuthorForm
    template_name = 'author/create_author_serve_side_in_datatable.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES)
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} registered.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} register.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:authors_list_serve_side_in_datetable')

class UpdateAuthorServerSideInDataTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, UpdateView):
    permission_required = ('user.change_author',)
    model = Author
    form_class = AuthorForm
    template_name = 'author/update_author_serve_side_in_datatable.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES, instance=self.get_object())
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} updation.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} updation.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:authors_list_serve_side_in_datetable')

class DeleteAuthorServerSideInDataTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, DeleteView):
    permission_required = ('user.delete_author',)
    model = Author
    template_name = 'author/delete_author.html'

    def delete(self, request, *args, **kwargs):
        if is_ajax(request):
            author = self.get_object()
            # elimination direct.
            author.delete()
            # logical elimination.
            # author.is_active = False
            # author.save()
            message = f'Successfully {self.model.__name__} elimination.'
            error = 'There are no errors.'
            response = JsonResponse({'message':message, 'error':error})
            response.status_code = 204
            return response
        else:
            redirect('book:authors_list_serve_side_in_datetable')

#Section of Books.
class BooksList(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, TemplateView):
    permission_required = ('user.view_book', 'user.add_book', 'user.change_book', 'user.delete_book')
    template_name = 'book/books_table.html'

class BooksTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, ListView):
    permission_required = ('user.view_book', 'user.add_book', 'user.change_book', 'user.delete_book')
    model = Book

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serialize('json', self.get_queryset(), use_natural_foreign_keys=True), 'application/json')
        else:
            return redirect('book:books_list')

class CreateBook(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, CreateView):
    permission_required = ('user.add_book',)
    model = Book
    form_class = BookForm
    template_name = 'book/create_book.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES)
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} registered.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} register.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:books_list')

class UpdateBook(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, UpdateView):
    permission_required = ('user.change_book',)
    model = Book
    form_class = BookForm
    template_name = 'book/update_book.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.form_class(request.POST, request.FILES, instance=self.get_object())
            if (form.is_valid()):
                form.save()
                message = f'Successfully {self.model.__name__} updation.'
                error = 'There are no errors.'
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 201
                return response
            else:
                message = f'Errorful {self.model.__name__} updation.'
                error = form.errors
                response = JsonResponse({'message':message, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('book:books_list')

class DeleteBook(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, UserPermissionRequiredMixin, DeleteView):
    permission_required = ('user.delete_book',)
    model = Book
    template_name = 'book/delete_book.html'

    def delete(self, request, *args, **kwargs):
        if is_ajax(request):
            book = self.get_object()
            # elimination direct.
            book.delete()
            # logical elimination.
            # book.is_active = False
            # book.save()
            message = f'Successfully {self.model.__name__} elimination.'
            error = 'There are no errors.'
            response = JsonResponse({'message':message, 'error':error})
            response.status_code = 204
            return response
        else:
            return redirect('book:books_list')

#Section of Reservations.
class AvailableBooks(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, ListView):
    model = Book
    paginate_by = 6
    template_name = 'book/available_books.html'

    def get_queryset(self):
        # greater than -> gt -> mayor que.
        # less than -> lt -> menor que.
        # less than -> lte -> menor igual que.
        return self.model.objects.filter(amount__gte=1) # greater than -> gte -> mayor igual que.

class AvailableBookDetail(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, DetailView):
    model = Book
    template_name = 'book/available_book_detail.html'

    def get(self, request, *args, **kwargs):
        if (self.get_object().amount > 0):
            return render(request, self.template_name, {'object': self.get_object()})
        return redirect('book:available_books')

class ReservationRegister(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, CreateView):
    model = Reservation
    success_url = reverse_lazy('book:available_books')

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            user = request.user
            book = Book.objects.filter(id = request.POST.get('book')).first()
            if (user and book):
                if (book.amount > 0):
                    new_reservation = self.model(
                        book = book,
                        user = user
                    )
                    new_reservation.save()
                    message = f'Successfully {self.model.__name__} registered.'
                    error = 'There are no errors.'
                    response = JsonResponse({'message':message, 'error':error, 'url': self.success_url})
                    response.status_code = 201
                    return response
        return redirect('book:available_books')

class BooksReservationsList(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, ListView):
    model = Reservation
    template_name = 'book/books_reservations_table.html'

    def get_queryset(self):
        return self.model.objects.filter(status=True, user=self.request.user)

class BooksReservationsTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, ListView):
    model = Reservation

    def get_queryset(self):
        return self.model.objects.filter(status=True, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_reservations'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serialize('json', self.get_queryset(), use_natural_foreign_keys=True), 'application/json')
        else:
            return redirect('book:books_reservations_list')

class ExpiredReservationsList(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, TemplateView):
    template_name = 'book/expired_reservations_table.html'

class ExpiredReservationsTable(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, ListView):
    model = Reservation

    def get_queryset(self):
        return self.model.objects.filter(status=False, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expired_reservations'] = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        if is_ajax(request):
            return HttpResponse(serialize('json', self.get_queryset(), use_natural_foreign_keys=True), 'application/json')
        else:
            return redirect('book:expired_reservations_list')