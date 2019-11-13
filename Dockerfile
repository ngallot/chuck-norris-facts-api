# Pull official fastapi image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install all dependencies
ADD requirements.txt ./requirements.txt
RUN pip install --upgrade pip -r requirements.txt

# Import config file
COPY ./config /app/config

# Install app
COPY app /app/app

ENTRYPOINT /start-reload.sh
