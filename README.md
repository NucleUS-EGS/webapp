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

4. Create a `.env` file with the information of the database

```bash
# DATABASE
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=db_port

# SERVICES
AUTH_SERVICE_URL=http://localhost:3001
AUTH_SERVICE_KEY=auth_service_key
EVENT_SERVICE_URL=http://localhost:3002
EVENT_SERVICE_KEY=event_service_key
POINTS_SERVICE_URL=http://localhost:3003
POINTS_SERVICE_KEY=points_service_key
```

5. Run the migrations

```bash
python3 manage.py migrate
```

6. Run the server

```bash
python3 manage.py runserver 3000
```

The **web app** should be running at `http://localhost:3000/`.  
The **db adminer** should be running at `http://localhost:8080/`.

The **database** host should be `127.0.0.1` and the port should be `3307`.