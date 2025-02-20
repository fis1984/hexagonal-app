
class UserNotFoundError(Exception):
    def __init__(self, id: int):
        super().__init__(f"User with ID {id} not found")