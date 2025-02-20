# src/application/handlers/create_user_handler.py
from application.commands.create_user_command import CreateUserCommand
from application.use_cases.create_user_use_case import CreateUserUseCase


class CreateUserHandler:
    def __init__(self, create_user_use_case: CreateUserUseCase):
        self.create_user_use_case = create_user_use_case

    async def handle(self, command: CreateUserCommand):
        return self.create_user_use_case.execute(name=command.name, email=command.email)