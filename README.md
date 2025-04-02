
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

## Technologies Used

- **Python 3.9**: Core programming language
- **Flask**: Lightweight web framework
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **CSV**: Simple data persistence

## Running the Application

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- Git

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YaraDaraghmeh/Bazar.com-A-Multi-tier-Online-Book-Store-.git
   cd bazar-bookstore
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

- Your Name - [GitHub Profile](https://github.com/yourusername)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
