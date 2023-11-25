# piko-server-fastapi

Application for creating surveys in the form of contests.

You can access it here http://31.129.106.57:3001/

Also You can see the client implementation here https://github.com/mnsavag/piko-client-react/

### Main stack

- Python
- Fastapi
- PostgreSQL
- SQLAlchemy
  
### Interacting with app (client)

#### Home Page

All polls are here. You can go through them by clicking the "start" button.

Or see the rating by clicking the "show result" button.

**Example**

![alt text](https://github.com/mnsavag/piko-server-fastapi/blob/master/site-home-page.png?raw=true)

#### Create Championship Page

Here you can create your survey. Available image formats: png/jpg/jpeg.

At the moment the editor preview does not correspond to the real preview.
​
### Swagger API

#### /docs

### Database view

![alt text](https://github.com/mnsavag/piko-server-fastapi/blob/master/piko-db.png?raw=true)

### Installation

Install dependencies

```bash
$ pip install -r requirements.txt
```
Use PostgerSQL

Set up the env variables in file **.env**

```bash
# set up database
$ alembic upgrade head
```

```bash
# database initialization
$ INSERT INTO category(name)
$ VALUES ('music');
$ INSERT INTO category(name)
$ VALUES ('cinema');
$ INSERT INTO category(name)
$ VALUES ('sport');
$ INSERT INTO category(name)
$ VALUES ('technology');
$ INSERT INTO category(name)
$ VALUES ('fashion');
$ INSERT INTO category(name)
$ VALUES ('nature');
$ INSERT INTO category(name)
$ VALUES ('games');
$ INSERT INTO category(name)
$ VALUES ('other');
```

### Running the app

```bash
# run app
$ uvicorn src.main:app --reload
```
