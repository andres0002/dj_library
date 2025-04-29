# py
from datetime import timedelta
# django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# third
# own
from apps.book.models import Author, Book, Reservation

# 1. forma de implementa los signals with el decorator @reciver(signal,sender=model).
@receiver(post_save, sender=Reservation)
def manage_reservation_seve(sender, instance, created, **kwargs):
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
        if not instance.is_avtive:
            book = instance.book
            Book.objects.filter(pk=book.pk).update(amount=book.amount + 1)

@receiver(post_save, sender=Author)
def manage_author_save(sender, instance, created, **kwargs):
    # creation.
    if created:
        print("Author created")
    # updation.
    else:
        if not instance.is_active:
            books = Book.objects.filter(author_id=instance.pk)
            for book in books:
                book.author_id.remove(instance.pk)

# elimination direct.
@receiver(post_delete, sender=Reservation)
def manage_reservation_delete(sender, instance, **kwargs):
    book = instance.book
    Book.objects.filter(pk=book.pk).update(amount=book.amount + 1)

# 2. forma de implementar los signals with signal.connect(function, sender=model).
# reducir el amount si se reserva un book.
def reduce_book_amount(sender, instance, **kwargs):
    book = instance.book
    if (book.amount > 0):
        # book.amount -= 1
        # book.save() # se recomienda con un update o una bandera, ya que el seve puede causar un signal recursivo (infinito).
        Book.objects.filter(pk=book.pk).update(amount=book.amount - 1)

# asignation de expiration date si no exist.
def add_expired_date_reservation(sender, instance, **kwrags):
    if (instance.expiration_date is None):
        instance.expiration_date = instance.create_date + timedelta(days=instance.amount_days)
        # instance.save() # se recomienda con un update o una bandera, ya que el seve puede causar un signal recursivo (infinito).
        Reservation.objects.filter(pk=instance.pk).update(expiration_date=instance.expiration_date)

# elimination logical del author.
def delete_relation_author_with_book(sender, instance, **kwargs):
    if not instance.is_active:
        books = Book.objects.filter(author_id=instance.pk)
        for book in books:
            book.author_id.remove(instance.pk) # el remove no acciona signals.

post_save.connect(reduce_book_amount, sender=Reservation)
post_save.connect(add_expired_date_reservation, sender=Reservation)
post_save.connect(delete_relation_author_with_book, sender=Author)