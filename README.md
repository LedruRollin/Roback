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

- Add documentation for exposed routes with a tool like Swagger
- Makes the app easily retrievable and ran locally with a containerization tool like Docker

# Run the project (*WIP section*)

You can retrieve the project via :

```bash
git clone https://github.com/LedruRollin/Roback.git
```
