# Domain Model

This page describes the core domain entities and their relationships within the application. The domain model represents the business concepts and rules at the heart of the system.

## Entity Relationship Diagram

```
+-------+       +------------+       +---------+
|  User |<----->| Cart       |<----->|Cart Item|
+-------+       +------------+       +---------+
    |                |                    |
    |                |                    |
    v                v                    v
+-------+       +------------+       +---------+
| Order |<----->| Payment    |<----->| Product |
+-------+       +------------+       +---------+
    |                                     |
    |                                     |
    +----------------+--------------------+
                     |
                     v
                 +---------+
                 |  Offer  |
                 +---------+
```

## Core Entities

### User Entity

The User entity represents users of the application.

**Key Attributes:**
- ID (UUID)
- Name
- Email
- Password (hashed)
- Gender (enum: MALE, FEMALE, OTHER)
- Birth date
- Created at
- Updated at

**Business Rules:**
- Email must be unique and in a valid format
- Password must meet security requirements
- User must be of legal age

### Product Entity

The Product entity represents items that can be purchased.

**Key Attributes:**
- ID (UUID)
- Name
- Description
- Price
- Category (enum: ELECTRONICS, CLOTHING, FOOD, etc.)
- Stock quantity
- Created at
- Updated at

**Business Rules:**
- Price must be positive
- Stock quantity must be non-negative
- Product name cannot be empty

### Cart Entity

The Cart entity represents a shopping cart for a user.

**Key Attributes:**
- ID (UUID)
- User ID (reference)
- Items (list of Cart Items)
- Created at
- Updated at

**Business Rules:**
- A user can have only one active cart
- Cart total must be calculated correctly from items

### Cart Item Entity

The Cart Item entity represents individual items in a cart.

**Key Attributes:**
- ID (UUID)
- Cart ID (reference)
- Product ID (reference)
- Quantity
- Created at
- Updated at

**Business Rules:**
- Quantity must be positive
- Cannot exceed available product stock

### Offer Entity

The Offer entity represents promotional offers for products.

**Key Attributes:**
- ID (UUID)
- Product ID (reference)
- Discount amount
- Type (enum: PERCENTAGE, FIXED_AMOUNT)
- Start date
- End date
- Created at
- Updated at

**Business Rules:**
- Discount must be positive
- End date must be after start date
- Offer must be valid during application

### Order Entity

The Order entity represents a customer's purchase.

**Key Attributes:**
- ID (UUID)
- User ID (reference)
- Items (list of products)
- Total amount
- Status (enum: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)
- Type (enum: STANDARD, EXPRESS)
- Created at
- Updated at

**Business Rules:**
- Order total must match sum of items
- Status transitions must follow a valid sequence
- Cannot be created with empty items list

### Payment Entity

The Payment entity represents payment information for an order.

**Key Attributes:**
- ID (UUID)
- Order ID (reference)
- Amount
- Method (enum: CREDIT_CARD, DEBIT_CARD, BANK_TRANSFER, etc.)
- Card Gateway (enum: PAYPAL, STRIPE, etc.)
- Status (enum: PENDING, PROCESSING, COMPLETED, FAILED, REFUNDED)
- Created at
- Updated at

**Business Rules:**
- Payment amount must match order total
- Status transitions must follow business rules
- Payment method must be valid

## Value Objects

In addition to entities, the domain model includes value objects:

- **Address**: Represents a physical address (Street, City, State, etc.)
- **Money**: Represents monetary values with currency
- **Email**: Represents a validated email address
- **Phone Number**: Represents a validated phone number

## Domain Services

The domain model also includes services that operate on multiple entities:

- **Cart Calculator**: Calculates cart totals including discounts
- **Stock Checker**: Validates product availability
- **Order Processor**: Handles the order lifecycle

## Repository Interfaces

Each entity has a corresponding repository interface that defines methods for persistence:

- **UserRepository**: Manages User entity persistence
- **ProductRepository**: Manages Product entity persistence
- **CartRepository**: Manages Cart entity persistence
- **CartItemRepository**: Manages CartItem entity persistence
- **OfferRepository**: Manages Offer entity persistence
- **OrderRepository**: Manages Order entity persistence
- **PaymentRepository**: Manages Payment entity persistence