# py
# django
from django.contrib import messages
# third
# own

# Definir action.
def elimination_from_actions_py_Authors_by_filter(model_admin, request, queryset): # actions en admin.
    if not request.user.has_perm(('app.can_mark_as_read',)): # permissions
        messages.error(request, "No tienes permiso para marcar como leído.")
        return
    # queryset = queryset.exclude(name__icontains='author') # i -> indistinto de mayúsculas y minúsculas, contains -> que contengo lo indicado.
    # for author in queryset:
    #     author.delete()
    # puedes mostrar un mensaje al usuario -> otra forma.
    model_admin.message_user(request, "Authors successfully removed -> message_user.")
    # puedes mostrar un mensaje al usuario -> types.
    messages.success(request, "Authors successfully removed.")
    messages.error(request, "Authors errorfully removed.")
    messages.warning(request, "Authors warningfully removed.")
    messages.info(request, "Authors infofully removed.")
    print(messages.debug(request, "Authors debugfully removed."))