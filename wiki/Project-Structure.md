# Project Structure

This page provides a detailed overview of the project's file and directory structure, helping developers understand how the codebase is organized.

## Directory Structure Overview

```
app-tcc-mba-uspesalq/
├── src/                    # Main source code
│   ├── domain/             # Domain entities and business rules
│   ├── usecases/           # Application use cases
│   └── infrastructure/     # External interfaces and implementations
├── tests/                  # Test files
├── docker-compose.yaml     # Docker Compose configuration
├── Dockerfile              # Docker build configuration
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Python project configuration
├── prometheus.yml          # Prometheus configuration
└── README.md               # Project documentation
```

## Detailed Structure

### Source Code (`src/`)

#### Domain Layer (`src/domain/`)

The domain layer contains the core business logic and entities:

```
domain/
├── __init__.py
├── __seedwork/              # Common domain utilities
│   ├── __init__.py
│   ├── test_utils.py        # Testing utilities
│   └── use_case_interface.py # Base interface for use cases
├── cart/                    # Cart domain
│   ├── __init__.py
│   ├── cart_entity.py       # Cart entity definition
│   ├── cart_repository_interface.py # Repository interface
│   └── test_cart_entity.py  # Tests for cart entity
├── cart_item/               # Cart item domain
│   ├── cart_item_entity.py
│   ├── cart_item_repository_interface.py
│   └── test_cart_item_entity.py
├── offer/                   # Offer domain
│   ├── offer_entity.py
│   ├── offer_repository_interface.py
│   ├── offer_type_enum.py
│   └── test_offer_entity.py
├── order/                   # Order domain
│   ├── order_entity.py
│   ├── order_repository_interface.py
│   ├── order_status_enum.py
│   ├── order_type_enum.py
│   └── test_order_entity.py
├── payment/                 # Payment domain
│   ├── payment_card_gateway_enum.py
│   ├── payment_entity.py
│   ├── payment_method_enum.py
│   ├── payment_repository_interface.py
│   ├── payment_status_enum.py
│   └── test_payment_entity.py
├── product/                 # Product domain
│   ├── product_category_enum.py
│   ├── product_entity.py
│   ├── product_repository_interface.py
│   └── test_product_entity.py
└── user/                    # User domain
    ├── test_user_entity.py
    ├── user_entity.py
    ├── user_gender_enum.py
    └── user_repository_interface.py
```

#### Use Cases Layer (`src/usecases/`)

The use cases layer implements application-specific business logic:

```
usecases/
├── __init__.py
├── cart/                    # Cart use cases
├── cart_item/               # Cart item use cases
├── offer/                   # Offer use cases
├── order/                   # Order use cases
├── payment/                 # Payment use cases
├── product/                 # Product use cases
└── user/                    # User use cases
```

#### Infrastructure Layer (`src/infrastructure/`)

The infrastructure layer implements interfaces to external systems:

```
infrastructure/
├── __init__.py
├── logging_config.py        # Logging configuration
├── api/                     # API implementation
│   ├── cache.py             # API caching mechanism
│   ├── config.py            # API configuration
│   ├── database.py          # Database connection management
│   ├── main.py              # API entry point
│   ├── test_database.py     # Database tests
│   ├── unit_of_work.py      # Unit of work pattern
│   └── consumers/           # API consumers/controllers
├── cart/                    # Cart infrastructure
├── cart_item/               # Cart item infrastructure
├── messaging/               # Messaging components
├── observability/           # Monitoring and observability
├── offer/                   # Offer infrastructure
├── order/                   # Order infrastructure
├── payment/                 # Payment infrastructure
├── product/                 # Product infrastructure
└── user/                    # User infrastructure
```

### Test Files (`tests/`)

```
tests/
└── fixtures/                # Test fixtures
```

### Configuration Files

- **docker-compose.yaml**: Defines services, networks, and volumes for Docker
- **Dockerfile**: Instructions for building the Docker image
- **requirements.txt**: Python package dependencies
- **pyproject.toml**: Python project metadata and configuration
- **prometheus.yml**: Configuration for Prometheus monitoring
- **pytest.ini**: PyTest configuration for running tests

## File Naming Conventions

- Entity files: `*_entity.py`
- Repository interfaces: `*_repository_interface.py`
- Enumerations: `*_enum.py`
- Tests: `test_*.py`
- Configuration: `*_config.py`

## Module Responsibilities

### Domain Modules

Each domain module contains:
- An entity class representing the core business object
- A repository interface defining how to access and manipulate entities
- Enum classes for valid entity states or categories
- Unit tests for the entity

### Use Case Modules

Each use case module contains:
- Use case implementations for specific business operations
- DTOs for transferring data between layers
- Converters for transforming between entities and DTOs

### Infrastructure Modules

Each infrastructure module contains:
- Repository implementations for the corresponding domain
- API controllers for handling external requests
- Database models/schemas
- External service integrations