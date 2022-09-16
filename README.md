# S3 Bucket Finder Web

## Instructions for launching the application locally

### 1. Clone the repository.

### 2. Create a virtual environment once in the project directory and active it.

```
    virtualenv .venv
```

```
    source .venv/bin/activate
```

### 3. Install the requirements.

```
    pip install -r requirements.txt
```

### 4. Create an .env file in the directory website/core/business/use_cases/aws/ which will contain the following information that you will need to provide.

```
    AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
    AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
    AWS_DEFAULT_REGION=<YOUR_AWS_DEFAULT_REGION>
```

### 5. Create another .env file in the directory website/core/business/use_cases/github/ which will contain the following information that you will need to provide.

```
    GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
```

### 6. Run the server.

```
    python manage.py runserver
```
