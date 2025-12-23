# Corre y ejecuta el ambiente virtual

```sh
python3 -m venv venv curso-fastapi
source curso-fastapi/bin/activate
```

# Instalar Fast API

```sh
pip install "fastapi[standard]"
```

# Crear carpeta para poder contener primer endpoint

```sh
mkdir ...
cd ...
code ...
```

# Abrir nuevamente al entorno virtual desde carpeta "curso-fa" (en este caso)

```sh
source ../curso-fastapi/bin/activate
```

# Para correr ejecuta:

```sh
fastapi dev
# api: http://localhost:8000/
# swagger: http://localhost:8000/docs
```

# Para correr un archivo especifico

```sh
fastapi dev main.py
fastapi dev time_stamp.py
```

# Para saber la versión de FastAPI

```sh
pip freeze | grep fast
```

# Para ejecutar la base de datos

```sh
sqlite3 db.sqlite3

# Para conocer las tablas

.tables

# Para valer valor en campo en customer

select * from customer;

# select * from customer;
# Luffy|Captain|Luffy@muhi.com|19|1
```
