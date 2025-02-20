# src/application/exceptions.py
class UserAlreadyExistsError(Exception):
    """Excepción lanzada cuando ya existe un usuario con el mismo correo electrónico."""
    pass