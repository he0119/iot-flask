# IOT-Flask

This is a submodule of iot project.

## Requirements

- Python 3.6+

## Getting Started

### CMD

Setup python environment

```bash
cd Flask
python -m venv venv
. venv/bin/activate(venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

Configuration

- Move ```application.cfg``` to ```instance``` floder and finish configuration
- Init database

```bash
flask db init
flask db migrate -m "init db"
flask db upgrade
flask create-user
```

Start server

```bash
flask run
```

### Docker

Init database

```bash
sudo docker run -it --rm -v ~/iot/instance:/app/instance he0119/iot-flask:latest flask db init
sudo docker run -it --rm -v ~/iot/instance:/app/instance he0119/iot-flask:latest flask db migrate -m "init db"
sudo docker run -it --rm -v ~/iot/instance:/app/instance he0119/iot-flask:latest flask db upgrade
sudo docker run -it --rm -v ~/iot/instance:/app/instance he0119/iot-flask:latest flask create-user
```

Use `Docker-Compose`

```shell
sudo docker-compose up -d
```

Now you can go to http://127.0.0.1:5000/
