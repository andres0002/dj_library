# django
from django.utils import timezone
# third
from datetime import timedelta
# own
from apps.book.models import Reservation

class ExpiredReservationMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (request.user.is_authenticated):
            current_date = timezone.now() - timedelta(hours=5)
            reservations = Reservation.objects.filter(status=True, user=request.user)
            for reservation in reservations:
                expired_date = reservation.createDate + timedelta(days=reservation.amount_days)
                if (current_date > expired_date):
                    reservation.status = False
                    reservation.save()