# django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
# third
# own

class LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated):
            # si es superuser, all permissions.
            if (request.user.is_superuser):
                return super().dispatch(request, *args, **kwargs)
            # si puede ingresar al admin de django, required permissions.
            elif (request.user.is_staff):
                return super().dispatch(request, *args, **kwargs)
            # si es user normal (is_active), solo puede ingresar al app web, required permissions.
            else:
                return super().dispatch(request, *args, **kwargs)
        return redirect('login')

class UserPermissionRequiredMixin(object):
    # para validar permissions no con el superuser, ya que no valida permissions.
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
        # valida si tiene los permissions si los tiene continue.
        if (request.user.has_perms(self.get_perms())):
            return super().dispatch(request, *args, **kwargs)
        # si no tiene los permissions te redireciona y te muestra message de error por permissions.
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect(self.get_url_redirect())

# ¿Qué tipo de mensaje es?
# Este mensaje es de tipo "error", que es uno de los niveles que Django soporta:
# El messages is temporal, si no se muestra estara presente hasta que se muestre como un context.
# pero si no se muestra tiene un tiempo de en el que se elimina si no se muestra.

# messages.debug(request, "%s SQL statements were executed." % count)
# messages.info(request, "Three credits remain in your account.")
# messages.success(request, "Profile details updated.")
# messages.warning(request, "Your account expires in three days.")
# messages.error(request, "Document deleted.")