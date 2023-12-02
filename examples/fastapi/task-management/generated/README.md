#   TaskManager

An application for managing tasks that enables multiple users to collaborate on a single project with multiple tasks.

Follow these steps to run the application:

## Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- [Python 3](https://www.python.org/downloads/)

## Installation and Setup

1. Create and activate a virtual environment:

```shell
python3 -m venv env
source env/bin/activate
```

2. Install the required Python packages:

```shell
pip install -r 'requirements.txt'
```

3. Start the FastAPI application:

```shell
uvicorn app.main:app --reload
```

4. Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)