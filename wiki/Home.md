# MBA USP-ESALQ TCC Project Wiki

Welcome to the official Wiki for the MBA USP-ESALQ TCC Project. This Wiki serves as the central documentation hub for the project, providing comprehensive information about the architecture, components, and how to interact with the system.

## Project Overview

This project is a TCC (Trabalho de Conclusão de Curso) developed for the MBA program at USP-ESALQ. The application follows a clean architecture approach with domain-driven design principles, separating concerns into domain entities, use cases, and infrastructure components.

## Table of Contents

1. [Architecture](#architecture)
2. [Project Structure](#project-structure)
3. [Domain Model](#domain-model)
4. [Setup and Installation](#setup-and-installation)
5. [Running Tests](#running-tests)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Infrastructure Components](#infrastructure-components)
9. [Messaging System](#messaging-system)
10. [Observability and Monitoring](#observability-and-monitoring)
11. [Docker Environment](#docker-environment)
12. [Contributing Guidelines](#contributing-guidelines)

## Architecture

The project follows a clean architecture pattern with distinct layers:

- **Domain Layer**: Contains business entities, repository interfaces, and business rules
- **Use Cases Layer**: Implements application-specific business rules
- **Infrastructure Layer**: Handles external concerns like databases, APIs, and messaging

This separation ensures the core business logic remains independent of external frameworks and systems, making the codebase more maintainable and testable.

See the [Architecture](Architecture) page for more details.

## Project Structure

```
src/
├── domain/           # Business entities and rules
├── usecases/         # Application use cases
└── infrastructure/   # External interfaces (DB, API, etc.)
    ├── api/          # API implementation
    ├── messaging/    # Messaging components
    └── observability/ # Monitoring and observability
```

See the [Project Structure](Project-Structure) page for more details.

## Domain Model

The domain layer contains the following key entities:

- **User**: Represents users of the system
- **Product**: Represents products that can be purchased
- **Cart**: Represents a shopping cart
- **Cart Item**: Represents items in a shopping cart
- **Offer**: Represents promotional offers
- **Order**: Represents customer orders
- **Payment**: Represents payment information

See the [Domain Model](Domain-Model) page for entity relationships and business rules.

## Setup and Installation

See the [Setup and Installation](Setup-and-Installation) page for instructions on setting up the development environment.

## Running Tests

Tests can be run using the provided PowerShell script:

```powershell
# Run all tests
.\run_tests.ps1

# Run a specific test file
.\run_tests.ps1 src/domain/cart/test_cart_entity.py
```

Alternatively, you can run tests manually:

```powershell
$env:PYTHONPATH = $PWD
python -m pytest src/domain/cart/test_cart_entity.py -v
```

See the [Testing Guide](Testing-Guide) page for more details.

## API Documentation

The API is built using FastAPI. See the [API Documentation](API-Documentation) page for endpoints and usage examples.

## Database Schema

The project uses a database schema as defined in the MySQL model files. See the [Database Schema](Database-Schema) page for details.

## Infrastructure Components

The infrastructure layer handles external interactions. See the [Infrastructure Components](Infrastructure-Components) page for details on:

- Database connections
- API implementation
- Caching mechanism
- Unit of work pattern

## Messaging System

The project includes a messaging system for asynchronous communication. See the [Messaging System](Messaging-System) page for details.

## Observability and Monitoring

The project uses Prometheus for monitoring. See the [Observability and Monitoring](Observability-and-Monitoring) page for details.

## Docker Environment

The project can be run using Docker and Docker Compose. See the [Docker Environment](Docker-Environment) page for details.

## Contributing Guidelines

See the [Contributing Guidelines](Contributing-Guidelines) page for information on how to contribute to the project.