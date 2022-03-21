### ETL Spotify - Postgresql

Creación de una ETL básica que consume la información de mis canciones escuchadas el día anterior en Spotify, realiza limpieza de la data y envía a una base de datos postgresql.

Para facilitar implementación de la base de datos, genero una base de datos Postgresql local en un contenedor docker con el comando:

```
docker run -d --name nombre_contenedor -v my_dbdata:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=contraseña_postgresql -e POSTGRES_USER=usuario_postgresql -e POSTGRES_DB=database_postgresql postgres
```

Corremos el contenedor:

```
docker exec -it nombre_contenedor psql -h localhost -U usuario_postgresql -W database_postgresql
```

Resultado de ejecución de ETL dentro de mi base de datos:

![Canciones escuchadas el 20 de marzo de 2022](/img/resultado.jpg)

Librerías utilizadas:

    - numpy==1.22.3
    - pandas==1.4.1
    - psycopg2-binary==2.9.3
    - python-dateutil==2.8.2
    - python-decouple==3.6
    - pytz==2022.1
    - requests==2.27.1
    - spotipy==2.19.0
    - SQLAlchemy==1.4.32
    - urllib3==1.26.9

WIP:

    - Implementación de Alembic
    - Implementar envío a base de datos con el ORM (Actualmente con pandas, SQLAlchemy solo establece conexión)