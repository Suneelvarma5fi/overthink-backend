# Overthink Backend

A backend application designed for the Overthink project.

---

## Installation Guide

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
Clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/Suneelvarma5fi/overthink-backend.git
cd overthink-backend
```

### 2. Setup Virtual Env

```bash
python -m venv new_env
source new_env/bin/activate   # macOS/Linux
new_env\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Provide Groq API Key

```bash
API_KEY = "your_api_key_here"
```


### 4. Run Application

```bash
python manage.py runserver
```

### 5. Sampel API Call


```bash
curl -X POST http://localhost:8000/create_root \
-H "Content-Type: application/json" \
-d '{
  "stateOutcome": "I want to start a new business.",
  "outComeID": 1
}'
```


