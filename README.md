# Intent

This project, `Roback`, is a basic CRUD app whose first goal was to learn the framework Django. It can not be considered as a ready-to-use production app, since key functionnalities are missing. However, it is functional and can be built locally (more info in the dedicated section)

# Vocabulary

- `Roback` : Name of the project
- `Search target` : Name for an entity holding a text in which search can be performed
- `Media` : Name for an entity which holds a piece of media, typically a video or an image

# Features

The main feature is to expose search targets. Each of these search targets holds a main text, and has optional media. There is a basic filtering implementation to perform text search across all search targets. For better performance, search targets access has been paginated.

# Front-end

The exposed data can be viewed in a dedicated UI. The code relative to this frontend can be found [here](https://github.com/LedruRollin/Rofront).

# Ideas of improvement

## Features
- Improve search system, which is currently minimal (a simple check by inclusion)
- Add tag support
- Add media processing : creation of thumbnails, transcoding

## Security

- Add authentification
- Add further safety checks for uploaded files
- Makes the app suitable and safe for production : hide secrets, add automatic error reports, add backup mechanism, add proper CI/CD, etc...
- Write the `pyproject.toml` file to setup build backend and project metadata ([link](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/))

## Quality of life

- ~~Add documentation for exposed routes with a tool like Swagger~~ (done, see [this commit](https://github.com/LedruRollin/Roback/commit/8e6ce42b8be01eec38a8c4c16a613334f555cc98))
- ~~Makes the app easily retrievable and ran locally with a containerization tool like Docker~~ (done, see [this commit](https://github.com/LedruRollin/Roback/commit/062ad4bd46f08baa78e0b9b6284f074b8ad54c6a))

# Run the project in standalone

This is a method to run the project in standalone, based on a local SQLite database. For a full build of the project  (front + PostgreSQL database, see dedicated section)
1) Retrieve the code

    You can retrieve the project via :

    ```bash
    cd my/projects/folder
    git clone https://github.com/LedruRollin/Roback.git
    cd Roback/
    ```

2) Setup the environment

    To run, the app needs some environment variables. To setup them, you can create a `.env` file inside project folder

    ```env
    # In file Roback/.env 
    ENGINE=django.db.backends.sqlite3
    NAME=rosearch
    MEDIA_ROOT=/home/roback/media
    MEDIA_URL=media/
    # To fill
    SECRET_KEY=''  
    ```

    The SECRET_KEY variable is used internally by Django to encrypt personal app data (more info in [the official doc](https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-SECRET_KEY)).
    You can generate your own by running this piece of code in a Django environment : 
    
    ```python3
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```

3) Launch the app

    To launch the app, use Docker to run it inside a container thanks to local `Dockerfile` :
    
    ```bash
    cd my/projects/folder/Roback
    docker build . -t roback-image:v1.0.0  # Build app image
    docker container run --name roback-container --env-file .env roback-image:v1.0.0   # Run container
    ```

Inside the container, you can then check everything's fine by retrieving seed data using the following commands :

```bash
apt-get install curl  # Install curl 
curl -i http://localhost:8000/api/search_targets/
```

# Run the whole project (WIP)

An easy way to launch the whole project is upcoming.
It will use Docker Compose to run the front, the back and the database.
