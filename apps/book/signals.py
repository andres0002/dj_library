# py
from datetime import timedelta
# django
from django.db.models.signals import post_save, post_delete, Signal, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
# third
# own
from apps.book.models import Author, Book, Reservation
from apps.base.utils.signals import prevent_signal_recursion

# 1. forma de implementa los signals with el decorator @reciver(signal,sender=model).
@receiver(pre_save, sender=Reservation)
@prevent_signal_recursion # para evitar recursion infinita de signals.
def manage_reservation_pre_seve(sender, instance, **kwargs): # para evitar que en el admin de django se ejecute la action si no hay books disponibles.
    book = instance.book
    if book.amount < 1:
        raise ValidationError('You cannot reservation this book, should exist available units.')

@receiver(post_save, sender=Reservation)
@prevent_signal_recursion # para evitar recursion infinita de signals.
def manage_reservation_post_seve(sender, instance, created, **kwargs):
    # creation
    if created:
        # reducir el stock del book.
        book = instance.book
        if book.amount > 0:
            Book.objects.filter(pk=book.pk).update(amount=book.amount - 1)
        # asignar fecha de expiración si no existe.
        if not instance.expiration_date:
            instance.expiration_date = instance.create_date + timedelta(days=instance.amount_days)
            # guardamos solo el campo modificado para evitar activar nuevamente el signal.
            Reservation.objects.filter(pk=instance.pk).update(expiration_date=instance.expiration_date)
    # updation.
    else:
        # elimination logical.
        if not instance.status:
            book = instance.book
            Book.objects.filter(pk=book.pk).update(amount=book.amount + 1)

# elimination direct.
@receiver(post_delete, sender=Reservation)
@prevent_signal_recursion # para evitar recursion infinita de signals.
def manage_reservation_post_delete(sender, instance, **kwargs):
    book = instance.book
    Book.objects.filter(pk=book.pk).update(amount=book.amount + 1)

@receiver(post_save, sender=Author)
@prevent_signal_recursion # para evitar recursion infinita de signals.
def manage_author_post_save(sender, instance, created, **kwargs):
    # creation.
    if created:
        pass
        # print("Author created")
    # updation.
    else:
        if not instance.is_active:
            books = Book.objects.filter(author_id=instance.pk)
            for book in books:
                book.author_id.remove(instance.pk)

# 2. forma de implementar los signals with signal.connect(function, sender=model).
# reducir el amount si se reserva un book.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def reduce_book_amount(sender, instance, **kwargs):
    book = instance.book
    if (book.amount > 0):
        # book.amount -= 1
        # book.save() # se recomienda con un update o una bandera, ya que el seve puede causar un signal recursivo (infinito).
        Book.objects.filter(pk=book.pk).update(amount=book.amount - 1)

# asignation de expiration date si no exist.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def add_expired_date_reservation(sender, instance, **kwrags):
    if (instance.expiration_date is None):
        instance.expiration_date = instance.create_date + timedelta(days=instance.amount_days)
        # instance.save() # se recomienda con un update o una bandera, ya que el seve puede causar un signal recursivo (infinito).
        Reservation.objects.filter(pk=instance.pk).update(expiration_date=instance.expiration_date)

# elimination logical del author.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def delete_relation_author_with_book(sender, instance, **kwargs):
    if not instance.is_active:
        books = Book.objects.filter(author_id=instance.pk)
        for book in books:
            book.author_id.remove(instance.pk) # el remove no acciona signals.

# post_save.connect(reduce_book_amount, sender=Reservation)
# post_save.connect(add_expired_date_reservation, sender=Reservation)
post_save.connect(delete_relation_author_with_book, sender=Author)

# signals custom.
user_registered = Signal() # user_registered -> signal.

@receiver(user_registered, sender=None) # el sender puede ser lo que se requiera.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def register_user(sender, user, **kwargs):
    print("Code signal.")
    user_registered.send(sender=None, user=user) # dispara nuevamente el signal y esto daría recursividad de signals.

@receiver(user_registered, sender="registro_web") # el sender puede ser lo que se requiera.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def web_registration_handler(sender, user, **kwargs):
    print(f"[WEB] Usuario registrado: {user.username}")
    user_registered.send(sender="registro_web", user=user) # dispara nuevamente el signal y esto daría recursividad de signals.

@receiver(user_registered, sender="registro_api") # el sender puede ser lo que se requiera.
@prevent_signal_recursion # para evitar recursion infinita de signals.
def api_registration_handler(sender, user, **kwargs):
    print(f"[API] Usuario registrado: {user.username}")
    user_registered.send(sender="registro_api", user=user) # dispara nuevamente el signal y esto daría recursividad de signals.

# 🔥 Así se dispara el signal custom, ya sea en el view o en el form.
# user_registered.send(sender=None, user=user)
# user_registered.send(sender="registro_web", user=user)
# user_registered.send(sender="registro_api", user=user)