FROM node:20 as static

WORKDIR /app
COPY ./static_src /app/static_src
COPY ./package*.json /app/
COPY ./webpack.config.js /app/

RUN npm install
RUN npm run build_release

FROM python:3.10
WORKDIR /code
COPY --from=static /app/static_compiled /static_compiled/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /code/

# This is inside the volume...
COPY requirements.txt /code/
RUN pip install -r requirements.txt
