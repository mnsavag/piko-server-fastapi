# piko-server-fastapi

Application for creating surveys in the form of contests.

You can access it here http://31.129.106.57:3001/

Also You can see the client implementation here https://github.com/mnsavag/piko-client-react/

## Main stack

- Python
- Fastapi
- PostgreSQL
- SQLAlchemy
​
## Swagger API

### URL address

```bash
/docs
```

### Preview

![alt text](https://github.com/mnsavag/piko-server-fastapi/blob/master/api-preview.png?raw=true)

## Database view

![alt text](https://github.com/mnsavag/piko-server-fastapi/blob/master/piko-db.png?raw=true)

## Installation

### Set environment variables

Create an .env file on src folder and copy the content from .env.example. Feel free to change it according to your own configuration.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up database

Use PostgreSQL

```bash
alembic upgrade head
```
 Database initialization
 
```bash
INSERT INTO category(name)
VALUES ('music');
INSERT INTO category(name)
VALUES ('cinema');
INSERT INTO category(name)
VALUES ('sport');
INSERT INTO category(name)
VALUES ('technology');
INSERT INTO category(name)
VALUES ('fashion');
INSERT INTO category(name)
VALUES ('nature');
INSERT INTO category(name)
VALUES ('games');
INSERT INTO category(name)
VALUES ('other');
```

### Running the app

```bash
uvicorn src.main:app --reload
```
