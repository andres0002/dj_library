# py
# djnago
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
# third
# own
from apps.book.models import Author
from apps.book.forms import AuthorForm

class AuthorFormset(FormView):
    template_name = 'author/author_formset.html'
    form_class = formset_factory(AuthorForm, extra=1)
    success_url = reverse_lazy('book:authors_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_form()
        return context
    
    def form_valid(self, formset):
        for form in formset:
            if form.is_valid():
                print(form.cleaned_data)
        return super().form_valid(formset)