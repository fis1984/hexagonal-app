
Autor: **Carlos Alberto Fis Fernández**

# Arquitectura Hexagonal con FastAPI: Guía Completa

---
En esta guía, exploraremos en detalle la implementación de una aplicación siguiendo la arquitectura hexagonal (también conocida como Ports and Adapters ) utilizando FastAPI , SQLAlchemy , Dependency Injector , Pydantic , y otros componentes clave. Esta arquitectura está diseñada para separar las capas de negocio de las dependencias externas, lo que permite un sistema más modular, testeable y mantenible.

---

<br>

# Índice

- [Arquitectura Hexagonal con FastAPI: Guía Completa](#arquitectura-hexagonal-con-fastapi-guía-completa)
- [Índice](#índice)
- [Introducción a la Arquitectura Hexagonal](#introducción-a-la-arquitectura-hexagonal)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Componentes Principales](#componentes-principales)
  - [Core](#core)
    - [Entidades (```entities/user.py ```)](#entidades-entitiesuserpy-)
    - [Puertos (```ports/i_user_repository.py```)](#puertos-portsi_user_repositorypy)
    - [Casos de Uso (```use_cases/create_user_use_case.py```)](#casos-de-uso-use_casescreate_user_use_casepy)
  - [Application](#application)
    - [Comandos (```commands/create_user_command.py```)](#comandos-commandscreate_user_commandpy)
    - [Mediador (`mediator/mediator.py`)](#mediador-mediatormediatorpy)
  - [Infrastructure](#infrastructure)
    - [Repositorio (`persistence/user_repository.py`)](#repositorio-persistenceuser_repositorypy)
  - [Presentation](#presentation)
- [Diagrama de Arquitectura](#diagrama-de-arquitectura)
- [Explicación Detallada de Cada Componente](#explicación-detallada-de-cada-componente)
- [Comandos para Ejecutar la Aplicación](#comandos-para-ejecutar-la-aplicación)


# Introducción a la Arquitectura Hexagonal


La arquitectura hexagonal es un patrón de diseño que promueve la separación entre el dominio de la aplicación (lógica de negocio) y las dependencias externas (bases de datos, frameworks web, etc.). Esto se logra mediante:

Puertos : Interfaces que definen cómo interactuar con el dominio.
Adaptadores : Implementaciones concretas de los puertos que conectan el dominio con el mundo exterior.

# Estructura del Proyecto


```
src/
├── config/
│   └── settings.py
├── core/
│   ├── entities/
│   │   └── user.py
│   ├── ports/
│   │   ├── i_user_repository.py
│   │   └── i_unit_of_work.py
│   └── use_cases/
│       ├── create_user_use_case.py
│       ├── get_user_by_id_use_case.py
│       └── list_users_use_case.py
├── application/
│   ├── commands/
│   │   └── create_user_command.py
│   ├── queries/
│   │   ├── get_user_by_id_query.py
│   │   └── list_users_query.py
│   ├── mediator/
│   │   └── mediator.py
│   └── handlers/
│       ├── create_user_handler.py
│       ├── get_user_by_id_handler.py
│       └── list_users_handler.py
├── infrastructure/
│   ├── persistence/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── user_repository.py
│   │   └── unit_of_work.py
│   ├── email/
│   │   └── email_service.py
│   └── web/
│       └── controllers/
│           └── user_controller.py
├── presentation/
│   └── main.py
├── middleware/
│   └── error_handler_middleware.py
└── errors/
    └── custom_errors.py
```

<br>

# Componentes Principales

## Core
El Core contiene la lógica de negocio pura, desacoplada de cualquier tecnología específica. Aquí definimos las entidades, puertos y casos de uso.

### Entidades (```entities/user.py ```)

Las `entidades` representan los objetos principales del dominio. En este caso, tenemos la entidad **User**.

```
from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    name: str
    email: str
```

### Puertos (```ports/i_user_repository.py```)

Los **puertos** son interfaces que definen cómo interactuar con el dominio. Por ejemplo, el puerto ```IUserRepository``` define métodos para acceder a los usuarios.

### Casos de Uso (```use_cases/create_user_use_case.py```)

Los **casos de uso** encapsulan la lógica de negocio. Por ejemplo, el caso de uso ```CreateUserUseCase``` maneja la creación de un usuario.

```from src.core.entities.user import User
from src.core.ports.i_user_repository import IUserRepository
from src.core.ports.i_unit_of_work import IUnitOfWork

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository, unit_of_work: IUnitOfWork):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    def execute(self, name: str, email: str) -> User:
        user = User(id=None, name=name, email=email)
        self.user_repository.create(user)
        self.unit_of_work.commit()
        return user
```

## Application

La capa **Application** actúa como intermediaria entre el **Core** y la **Infraestructura** . Aquí definimos comandos, consultas, mediador y manejadores.

### Comandos (```commands/create_user_command.py```)

Los **comandos** representan acciones específicas, como crear un usuario.

```
from pydantic import BaseModel

class CreateUserCommand(BaseModel):
    name: str
    email: str

```
### Mediador (`mediator/mediator.py`)

El **mediador** coordina la ejecución de comandos y consultas.

```
from typing import Type

class Mediator:
    def __init__(self):
        self._command_handlers = {}
        self._query_handlers = {}

    def register_command_handler(self, command_type: Type, handler):
        self._command_handlers[command_type] = handler

    async def send(self, command):
        handler = self._command_handlers[type(command)]
        return await handler.handle(command)

```

## Infrastructure

La capa **Infrastructure** contiene adaptadores para interactuar con tecnologías externas, como bases de datos y servicios de correo.

### Repositorio (`persistence/user_repository.py`)

El **repositorio** implementa el puerto `IUserRepository` usando SQLAlchemy.

```
from sqlalchemy.orm import Session
from src.core.entities.user import User
from src.core.ports.i_user_repository import IUserRepository
from src.infrastructure.persistence.models import UserModel

class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> None:
        db_user = UserModel(name=user.name, email=user.email)
        self.db_session.add(db_user)

```

Envío de Correos (`email/email_service.py`)

El servicio de correo envía correos electrónicos.

```
import smtplib
from email.mime.text import MIMEText
from src.config.settings import settings

class EmailService:
    def send_email(self, to_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_USER
        msg['To'] = to_email

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, [to_email], msg.as_string())
```

## Presentation

La capa **Presentation** expone la API REST usando FastAPI.

**Controladores** (`web/controllers/user_controller.py`)

Los controladores manejan las solicitudes HTTP.

Los **controladores** manejan las solicitudes HTTP.

```
from fastapi import APIRouter, Depends
from src.application.commands.create_user_command import CreateUserCommand
from src.application.mediator.mediator import Mediator
from src.infrastructure.container import Container

router = APIRouter()

@router.post("/")
async def create_user(command: CreateUserCommand, mediator: Mediator = Depends(Container.mediator)):
    return await mediator.send(command)
```

# Diagrama de Arquitectura

![arquitectura-hexagonal](https://raw.githubusercontent.com/fis1984/hexagonal-app/refs/heads/master/static/images/arquitectura-hexagonal.avif)



# Explicación Detallada de Cada Componente

Cada componente tiene un propósito específico:

 - Core : Contiene la lógica de negocio pura.
 - Application : Coordina la ejecución de casos de uso.
 - Infrastructure : Implementa adaptadores para tecnologías externas.
 - Presentation : Expone la API REST.


# Comandos para Ejecutar la Aplicación

1. Crear el entorno virtual:
   ``` 
    uv venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```
    uv pip install -r requirements.txt
   ```
3. Iniciar la aplicación:
   ```
    uv run python src/presentation/main.py
   ```
