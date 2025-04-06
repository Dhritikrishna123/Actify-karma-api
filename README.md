# Actify Karma System API

A FastAPI-based backend service for managing karma points and trust scores in the Actify ecosystem.

## Features

- Karma point management
- Trust score calculation
- User verification levels
- Transaction history
- Domain-specific karma tracking

## Tech Stack

- Python 3.8+
- FastAPI
- MongoDB Atlas
- Motor (Async MongoDB driver)
- Pydantic
- Uvicorn

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Dhritikrishna123/Actify-karma-api.git
cd actify-karma-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Update the `.env` file with your MongoDB Atlas credentials:
```
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=Karma-system-api
MONGODB_DB=karma_db
```

6. Run the development server:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
karma-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routers/
│   │       └── endpoints/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── schemas/
│   ├── tests/
│   ├── .env
│   ├── .gitignore
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 