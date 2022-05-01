FROM python:3.7
ARG GIT_HASH
ARG GIT_MODIFIED
RUN apt update && apt install -y sqlite3
WORKDIR /astro-tablets
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src
VOLUME /astro-tablets/generated
VOLUME /astro-tablets/skyfield-data
ENV GIT_HASH=$GIT_HASH
ENV GIT_MODIFIED=$GIT_MODIFIED
ENTRYPOINT ["python", "./src/cli.py"]
