# django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
# third
# own

class LoginRequiredUserIstaffOrIsactiveRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated):
            if (request.user.is_staff):
                return super().dispatch(request, *args, **kwargs)
            elif (request.user.is_active):
                return super().dispatch(request, *args, **kwargs)
        return redirect('index')

class UserPermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if (isinstance(self.permission_required,str)):
            return (self.permission_required)
        else:
            return self.permission_required

    def get_url_redirect(self):
        if (self.url_redirect is None):
            return reverse_lazy('login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if (request.user.has_perms(self.get_perms())):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect(self.get_url_redirect())