# FastAPI-Scrapper

FastAPI app with GraphQL (Strawberry) exposing user and item management. Database schema managed by Alembic migrations at startup.

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

#### Quick Setup (Linux/macOS)

1. Clone the repository:
```bash
git clone https://github.com/mathisbukowski/FastAPI-Scrapper.git
cd FastAPI-Scrapper
```

2. Run the setup script:
```bash
./setup.sh
```

#### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/mathisbukowski/FastAPI-Scrapper.git
cd FastAPI-Scrapper
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the project root (or export variables) with at least:

```
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=fastapi_scrapper
HOST=0.0.0.0
PORT=8000
APP_NAME=FastAPI-Scrapper
APP_VERSION=0.1.0
```

Ensure a PostgreSQL instance is running matching those credentials.

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

### Database Migrations (Alembic)

Alembic is configured and runs automatically on startup (`upgrade head`).
If you prefer manual control:

Generate a new revision (autogenerate based on model changes):
```bash
alembic revision --autogenerate -m "add new column"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback one step:
```bash
alembic downgrade -1
```

Show current head:
```bash
alembic current
```

Because the app runs `upgrade head` during startup, ensure your migrations are committed before deploying.

The API will be available at:

- Main application: http://localhost:8000
- GraphQL endpoint: http://localhost:8000/graphql
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

### GraphQL Usage

Example queries and mutations (use a GraphQL client or the Strawberry built-in interface at `/graphql`):

Query all users:
```graphql
query {
	users { id username email created_at }
}
```

Create a user:
```graphql
mutation {
	create_user(email: "john@example.com", username: "john") { id username }
}
```

Create an item for a user:
```graphql
mutation {
	create_item(user_id: 1, name: "Mon Item") { id name user_id }
}
```

List items for a user:
```graphql
query {
	items(user_id: 1) { id name created_at user_id }
}
```

Get user with nested items:
```graphql
query {
	user(user_id: 1) { id username items { id name } }
}
```

Delete an item:
```graphql
mutation {
	delete_item(item_id: 5)
}
```

## API Endpoints (REST)

- `GET /` - Welcome message

GraphQL operations replace dedicated REST endpoints for users/items in this project.

## Development

To deactivate the virtual environment when you're done:
```bash
deactivate
```