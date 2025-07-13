# Presentation Feedback System

A Django-based API that provides AI-powered feedback for presentations using Groq API and Llama model.

## Features

- Accepts text or file-based presentations
- Provides detailed feedback using Llama model
- RESTful API endpoints
- File upload support
- Feedback history storage

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with:
```
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key_here
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the server:
```bash
python manage.py runserver
```

## API Usage

### Get Presentation Feedback

**Endpoint:** `POST /api/feedback/`

**Request Body:**
- For text content:
```json
{
    "type": "text",
    "content": "Your presentation text here"
}
```

- For file upload:
```json
{
    "type": "file",
    "file": [binary file data]
}
```

**Response:**
```json
{
    "id": 1,
    "feedback": "Detailed feedback from the AI...",
    "created_at": "2024-03-14T12:00:00Z"
}
```

## Notes

- Maximum file size: 10MB
- Supported file types: Text files (.txt, .doc, .docx, etc.)
- The API uses the Llama 2 model through Groq API 