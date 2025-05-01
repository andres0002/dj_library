import threading # para manejar hilos.
from functools import wraps # para conservar data original de la función que la implementa.

# Diccionario de banderas thread-local por función
_signal_flags = threading.local()

def prevent_signal_recursion(func):
    """
    Decorador para evitar la recursión infinita en signals de Django.
    Marca la ejecución del signal y previene que se dispare nuevamente
    mientras esté en ejecución el primer signal.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Usamos el nombre del handler como clave única
        flag_name = f"_in_signal_{func.__name__}"
        
        # Verificamos si la bandera ya está activa
        if getattr(_signal_flags, flag_name, False):
            return  # Ya está en ejecución: evitar recursividad
        
        # Marcamos la bandera como True indicando que el signal está en ejecución
        setattr(_signal_flags, flag_name, True)
        
        try:
            return func(*args, **kwargs)  # Llamamos al handler original del signal
        finally:
            # Después de ejecutar el signal, limpiamos la bandera
            setattr(_signal_flags, flag_name, False)

    return wrapper