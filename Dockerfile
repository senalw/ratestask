FROM  postgres:12 as database
COPY resources/rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
ENV POSTGRES_USER=ratestask
ENV POSTGRES_PASSWORD=ratestask

FROM python:3.11-slim-bullseye as app
LABEL author='SenalW'
ARG USER="xeneta"
ARG GROUP="xeneta"
ARG UID=1001
ARG GID=1001

WORKDIR /ratetask

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install make -y

# Create a non-root user and group with specified UID and GID
RUN groupadd -r -g $GID $GROUP && useradd -d /ratetask -u $UID -r -g $USER $GROUP

# Set ownership of the working directory to the created user and group
RUN chown -R $USER:$GROUP /ratetask

USER $UID

COPY --chown=$USER:$GROUP Makefile .
COPY --chown=$USER:$GROUP requirements.txt .
COPY --chown=$USER:$GROUP requirements-style.txt .
COPY --chown=$USER:$GROUP settings.py .

RUN make setup

COPY --chown=$USER:$GROUP src ./src/
COPY --chown=$USER:$GROUP resources ./resources/

ENTRYPOINT ["make", "run"]
