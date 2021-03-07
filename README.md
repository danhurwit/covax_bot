# covax-bot

### pre-requisites
* Install docker
* Run RabbitMQ in docker `docker run -d -p 5672:5672 rabbitmq`
* create database [using this file](src/data/db_admin.py) `python db_admin.py` 
* set `DB_URL` and `DISCORD_WEBHOOK_URL` in `.env` file


### running manually
from within the top level directory
* start the beat scheduler `celery -A src.celery_app beat`
* start the workers `celery -A src.celery_app worker -l INFO`
* run once `celery call src.appointment_runner.run`

### run scheduled
* `overmind start (-D)`
* to tail logs: `overmind echo`

### within IDE
`python main.py`
