# Architecture

This project is built following the principles of Clean Architecture and Domain-Driven Design (DDD), emphasizing separation of concerns and business logic independence from external frameworks.

## Clean Architecture Overview

The application is structured in concentric layers, with dependencies pointing inward:

![Clean Architecture Diagram](https://lucid.app/publicSegments/view/4f25c5aa-62b9-468d-9e0f-5a5df6df1f1f/image.png)

1. **Domain Layer** (Innermost)
   - Contains business entities, repository interfaces, and domain rules
   - Has no dependencies on other layers or external frameworks
   - The core business logic resides here

2. **Use Case Layer**
   - Contains application-specific business rules
   - Depends only on the domain layer
   - Orchestrates the flow of data to and from entities

3. **Infrastructure Layer** (Outermost)
   - Contains implementations of interfaces defined in inner layers
   - Depends on external frameworks (databases, messaging, etc.)
   - Adapts external frameworks to the needs of the application

## Components

### Domain Layer

The domain layer is designed around these key components:

- **Entities**: Core business objects (User, Product, Cart, etc.)
- **Repository Interfaces**: Define how to access and manipulate entities
- **Value Objects**: Immutable objects representing concepts in the domain
- **Domain Services**: Encapsulate business operations that involve multiple entities

### Use Case Layer

The use case layer contains:

- **Use Case Classes**: Implement specific business operations
- **DTOs (Data Transfer Objects)**: Carry data between processes
- **Converters**: Transform between domain entities and DTOs

### Infrastructure Layer

The infrastructure layer includes:

- **Repository Implementations**: Database-specific implementations of repository interfaces
- **API Controllers**: Handle HTTP requests and responses
- **Messaging Components**: Implement message producers and consumers
- **Database Configuration**: Setup and connections to databases
- **Observability Tools**: Monitoring and logging systems

## Communication Flow

1. External requests enter through the infrastructure layer
2. Controllers/adapters transform input to a format usable by use cases
3. Use cases orchestrate the business operation using domain entities
4. Results flow back outward through the layers

## Benefits of This Architecture

- **Testability**: Core business logic can be tested independently of external frameworks
- **Flexibility**: External components can be replaced with minimal impact on business logic
- **Maintainability**: Clear separation of concerns makes the codebase easier to understand
- **Scalability**: Components can be developed and scaled independently