# Web Application for NucleUS

Application in Django for both the front-end web app and the API to serve it.

## Installation

1. Create a python virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the requirements

```bash
pip3 install -r requirements.txt
```

3. Run the default mysql database server with docker

```bash
docker-compose -f database.yml up -d
```

4. Run the migrations

```bash
python3 manage.py migrate
```

5. Run the server

```bash
python3 manage.py runserver
```

The **web app** should be running at `http://localhost:8000/`.  
The **db adminer** should be running at `http://localhost:8080/`.

The **database** host should be `127.0.0.1` and the port should be `3307`.