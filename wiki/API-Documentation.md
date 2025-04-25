# API Documentation

This page provides comprehensive documentation for the API endpoints available in the MBA USP-ESALQ TCC Project.

## API Overview

The API is built using FastAPI and follows RESTful principles. It provides endpoints for managing users, products, carts, orders, and payments.

### Base URL

When running locally, the API is available at:

```
http://localhost:8000
```

### Authentication

Most endpoints require authentication. The API uses JWT (JSON Web Tokens) for authentication.

#### Obtaining a Token

```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Using the Token

Include the token in the `Authorization` header for subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## API Endpoints

### User Endpoints

#### Register a New User

```
POST /api/users
```

Request body:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "gender": "MALE",
  "birth_date": "1990-01-01"
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "gender": "MALE",
  "birth_date": "1990-01-01",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

#### Get User Profile

```
GET /api/users/me
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "gender": "MALE",
  "birth_date": "1990-01-01",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

#### Update User Profile

```
PUT /api/users/me
```

Request body:
```json
{
  "name": "John Updated Doe",
  "email": "john.updated@example.com"
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Updated Doe",
  "email": "john.updated@example.com",
  "gender": "MALE",
  "birth_date": "1990-01-01",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-02T09:30:00Z"
}
```

### Product Endpoints

#### List Products

```
GET /api/products
```

Query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10)
- `category`: Filter by category
- `min_price`: Minimum price
- `max_price`: Maximum price
- `search`: Search term

Response:
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Smartphone XYZ",
      "description": "Latest smartphone model",
      "price": 999.99,
      "category": "ELECTRONICS",
      "stock_quantity": 100,
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "name": "T-Shirt",
      "description": "Cotton T-Shirt",
      "price": 19.99,
      "category": "CLOTHING",
      "stock_quantity": 200,
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 2
}
```

#### Get Product Details

```
GET /api/products/{product_id}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Smartphone XYZ",
  "description": "Latest smartphone model",
  "price": 999.99,
  "category": "ELECTRONICS",
  "stock_quantity": 100,
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Cart Endpoints

#### Get Current Cart

```
GET /api/cart
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Smartphone XYZ",
      "product_price": 999.99,
      "quantity": 1,
      "subtotal": 999.99
    }
  ],
  "total": 999.99,
  "created_at": "2023-01-02T10:00:00Z",
  "updated_at": "2023-01-02T10:00:00Z"
}
```

#### Add Item to Cart

```
POST /api/cart/items
```

Request body:
```json
{
  "product_id": "550e8400-e29b-41d4-a716-446655440001",
  "quantity": 1
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Smartphone XYZ",
      "product_price": 999.99,
      "quantity": 1,
      "subtotal": 999.99
    }
  ],
  "total": 999.99,
  "created_at": "2023-01-02T10:00:00Z",
  "updated_at": "2023-01-02T10:05:00Z"
}
```

#### Update Cart Item

```
PUT /api/cart/items/{item_id}
```

Request body:
```json
{
  "quantity": 2
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Smartphone XYZ",
      "product_price": 999.99,
      "quantity": 2,
      "subtotal": 1999.98
    }
  ],
  "total": 1999.98,
  "created_at": "2023-01-02T10:00:00Z",
  "updated_at": "2023-01-02T10:10:00Z"
}
```

#### Remove Cart Item

```
DELETE /api/cart/items/{item_id}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [],
  "total": 0,
  "created_at": "2023-01-02T10:00:00Z",
  "updated_at": "2023-01-02T10:15:00Z"
}
```

### Order Endpoints

#### Create Order

```
POST /api/orders
```

Request body:
```json
{
  "order_type": "STANDARD"
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Smartphone XYZ",
      "product_price": 999.99,
      "quantity": 2,
      "subtotal": 1999.98
    }
  ],
  "total": 1999.98,
  "status": "PENDING",
  "type": "STANDARD",
  "created_at": "2023-01-03T09:00:00Z",
  "updated_at": "2023-01-03T09:00:00Z"
}
```

#### List Orders

```
GET /api/orders
```

Query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10)
- `status`: Filter by status

Response:
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "total": 1999.98,
      "status": "PENDING",
      "type": "STANDARD",
      "created_at": "2023-01-03T09:00:00Z",
      "updated_at": "2023-01-03T09:00:00Z"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 1
}
```

#### Get Order Details

```
GET /api/orders/{order_id}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "product_id": "550e8400-e29b-41d4-a716-446655440001",
      "product_name": "Smartphone XYZ",
      "product_price": 999.99,
      "quantity": 2,
      "subtotal": 1999.98
    }
  ],
  "total": 1999.98,
  "status": "PENDING",
  "type": "STANDARD",
  "created_at": "2023-01-03T09:00:00Z",
  "updated_at": "2023-01-03T09:00:00Z"
}
```

### Payment Endpoints

#### Create Payment

```
POST /api/orders/{order_id}/payments
```

Request body:
```json
{
  "method": "CREDIT_CARD",
  "card_gateway": "STRIPE",
  "card_number": "4242424242424242",
  "card_expiry_month": 12,
  "card_expiry_year": 2025,
  "card_cvc": "123"
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "order_id": "550e8400-e29b-41d4-a716-446655440005",
  "amount": 1999.98,
  "method": "CREDIT_CARD",
  "card_gateway": "STRIPE",
  "status": "PROCESSING",
  "created_at": "2023-01-03T10:00:00Z",
  "updated_at": "2023-01-03T10:00:00Z"
}
```

#### Get Payment Details

```
GET /api/orders/{order_id}/payments/{payment_id}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "order_id": "550e8400-e29b-41d4-a716-446655440005",
  "amount": 1999.98,
  "method": "CREDIT_CARD",
  "card_gateway": "STRIPE",
  "status": "COMPLETED",
  "created_at": "2023-01-03T10:00:00Z",
  "updated_at": "2023-01-03T10:05:00Z"
}
```

## Error Responses

The API returns standard HTTP status codes and a consistent error response format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Common Error Codes

- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid input data
- `RESOURCE_NOT_FOUND`: Requested resource not found
- `INTERNAL_SERVER_ERROR`: Server encountered an unexpected error

## Rate Limiting

The API implements rate limiting to prevent abuse:

- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## API Versioning

The API is versioned through the URL path:

```
/api/v1/resources
```

When a new incompatible version is released, the URL path will be updated (e.g., `/api/v2/resources`).

## OpenAPI Documentation

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

The OpenAPI specification is available at:

```
http://localhost:8000/openapi.json
```