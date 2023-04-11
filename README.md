# FastAPI Tutorial
This repository is a comprehensive guide to API development using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.

In this repository, you'll learn how to build and deploy a complete API from scratch, covering all aspects of API development, from setting up a development environment to creating data models, defining API endpoints, testing, and deployment.

# How to use this repository
To follow this tutorial, you should have Python 3.6+ installed on your machine, along with pip.

To get started, clone this repository to your local machine and run:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running the project using Docker
To run the project using Docker, make sure you have Docker installed on your machine. Then, follow these steps:

The docker file is not ready yet. Will be posted very soon!

```bash
docker build -t my-fastapi-app .
```
```bash
docker run -p 8000:80 my-fastapi-app`
```

# Contributing
If you find any errors or want to contribute to this tutorial, feel free to create a pull request or an issue on the repository. Your contributions are highly appreciated!
