# py
import logging
# django
from django.utils import timezone
# third
from datetime import timedelta
# own
from apps.book.models import Reservation

logger = logging.getLogger('apps.book.middleware')

class ExpiredReservationMiddleware:
    # is required.
    def __init__(self, get_response):
        self.get_response = get_response
        # Se ejecuta una vez cuando se inicia el servidor.  

    # is required.
    def __call__(self, request):
        # Código que se ejecuta antes de que la vista se llame.
        response = self.get_response(request)
        # Código que se ejecuta después de que la vista se haya llamado.
        return response

    # process_view -> se llama o ejecuta antes (process_request) y despues (process_response) de la request.
    # process_view -> return: 
    # - non -> para que continues con la ejecución de los demas middleware.
    # - HttpResponse -> en ese caso no llama a mas middleware y responde al navegator,
    #   para este caso se debe tener bien presente donde se debe poner el middleware (settings.py) ya que no dejaría
    #   ejecutar los demas middleware que vengan despues.
    def process_view(self, request, view_func, view_args, view_kwargs):
        if (request.user.is_authenticated):
            # 1. forma, menos optima.
            # current_date = timezone.now()
            # reservations = Reservation.objects.filter(status=True, user=request.user)
            # for reservation in reservations:
            #     expired_date = reservation.create_date + timedelta(days=reservation.amount_days)
            #     if (current_date > expired_date):
            #         reservation.status = False
            #         reservation.save()
            # 2. forma, mas optima.
            current_date = timezone.now()
            # Buscar reservas activas que ya hayan expirado
            expired_reservations = Reservation.objects.filter(
                user=request.user,
                status=True,
                expiration_date__lt=current_date
            )
            # Desactivarlas de una vez
            updated_count = expired_reservations.update(status=False)
            # Registramos cuántos registros se actualizaron en el .log
            if updated_count > 0:
                logger.info(f'{updated_count} reservas expiradas para el usuario {request.user.username}.')
        
        # Ejemplo de diferentes niveles de log
        # logger.debug('Este es un mensaje DEBUG')
        # logger.info('Este es un mensaje INFO')
        # logger.warning('Este es un mensaje WARNING')
        # logger.error('Este es un mensaje ERROR')
        # logger.critical('Este es un mensaje CRITICAL')