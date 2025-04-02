
# Bazar.com: Multi-tier Online Book Store



## Overview

Bazar.com is a minimalist online bookstore implementing a multi-tier microservices architecture. The system consists of three primary components:

- **Frontend Service**: Handles user interactions and forwards requests
- **Catalog Service**: Manages book information and inventory
- **Order Service**: Processes purchases and maintains order history

The application uses Flask for the web framework with a REST API interface and Docker for containerization and deployment.

## Architecture


### Key Components

- **Frontend Tier**: Single service that accepts user requests for searching, viewing book details, and making purchases
- **Backend Tier**: 
  - Catalog Service: Maintains book information including stock levels, prices, and topics
  - Order Service: Handles purchase requests and maintains order history

### Features

- Search books by topic (distributed systems or undergraduate school)
- View detailed information about specific books
- Purchase books with inventory validation
- Persistent data storage using CSV files
- Containerized microservices for easy deployment

Technologies Used
Flask
Flask is a micro web framework written in Python that we've used for all three services. Some key aspects of how we've utilized Flask:

RESTful API Design: Created clear endpoint routes following REST principles for each service
Blueprint Organization: Logical organization of code for maintainability
Lightweight Processing: Minimal overhead for handling requests between microservices
JSON Response Handling: Standardized JSON responses across all API endpoints
Simple Request Processing: Used Flask's request object to handle incoming data

Flask was chosen for its simplicity and flexibility, making it ideal for microservices. It doesn't impose a specific structure or dependencies, allowing each service to be truly independent and focused on its specific responsibility.
Docker & Docker Compose
Docker containerization is used to package each microservice with its dependencies:

Isolated Environments: Each service runs in its own container with specific dependencies
Networking: Docker Compose creates a custom network allowing services to communicate by name
Volume Mapping: Persistent data is stored in mapped volumes for CSV files
Reproducibility: Consistent environment across development and deployment
Scalability: Services can be scaled independently as needed
Zero-Configuration Deployment: Environment variables and service discovery handled automatically

CSV for Data Storage
We've implemented a simple persistence layer using CSV files:

Lightweight: No database setup required
Human-Readable: Easy to inspect and modify data directly if needed
Portable: Data can be easily backed up or transferred
File Locking: Implemented to handle concurrent access
Schema Definition: Clear column definitions for data integrity

Python Libraries

Requests: HTTP library for service-to-service communication
Flask-CORS: Cross-Origin Resource Sharing support
CSV Module: Python's built-in CSV handling for data persistence
JSON: Used for standardized data exchange between services

## Running the Application

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- Git

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YaraDaraghmeh/Bazar.com-A-Multi-tier-Online-Book-Store-.git
   cd Bazar.com-A-Multi-tier-Online-Book-Store-
   ```

2. Build and start the containers:
   ```bash
   docker-compose build
   docker-compose up
   ```

3. The application will be available at:
   ```
   http://localhost:5002
   ```

### API Endpoints

#### Frontend Service (port 5002)
- `GET /api/search/<topic>`: Search books by topic
- `GET /api/info/<item_id>`: Get book details
- `POST /api/purchase/<item_id>`: Purchase a book

#### Catalog Service (port 5000)
- `GET /search/<topic>`: Search books by topic
- `GET /info/<item_id>`: Get book details
- `PUT /update/<item_id>`: Update book price or quantity

#### Order Service (port 5001)
- `POST /purchase/<item_id>`: Process book purchase

## Development

### Project Structure

```
bazar/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── catalog/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── data/
│       └── books.csv
└── order/
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    └── data/
        └── orders.csv
```

### Data Persistence

The application uses CSV files for persistent storage:

- `catalog/data/books.csv`: Stores book information
- `order/data/orders.csv`: Stores order history

## Testing

### Manual Testing

1. **Search Books**:
   - Select a topic from the dropdown
   - Click "Search"
   - View list of matching books

2. **View Book Details**:
   - Enter a book ID (1-4)
   - Click "Get Info"
   - View details including price and stock level

3. **Purchase Book**:
   - Enter a book ID (1-4)
   - Click "Purchase"
   - Confirm successful purchase message

### Sample Test Cases

| Test | Input | Expected Output |
|------|-------|----------------|
| Search by topic | "distributed systems" | Books 1 & 2 |
| Get book info | ID: 3 | Title, price, and quantity for "Xen and the Art of Surviving Undergraduate School" |
| Purchase a book | ID: 1 | Success message and reduced inventory count |
| Purchase out-of-stock book | ID of out-of-stock book | Error message |

## Design Decisions & Tradeoffs

- **CSV over Database**: Chose CSV files for simplicity and portability, sacrificing query performance
- **Microservice Architecture**: Enables independent scaling and development but adds network complexity
- **Docker Containerization**: Ensures consistent environments but requires Docker knowledge
- **Flask**: Lightweight framework that's easy to learn but lacks some features of larger frameworks

## Extending the Project

Potential enhancements:

- Add user authentication system
- Implement a shopping cart feature
- Add a database backend (e.g., SQLite)
- Create admin interface for inventory management
- Add unit and integration tests
- Implement CI/CD pipeline

## Contributors

- Yara - (https://github.com/YaraDaraghmeh)
- Shams - (https://github.com/ShamsAziz03)


