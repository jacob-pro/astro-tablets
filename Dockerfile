FROM python:3.5.10
ARG GIT_HASH
RUN apt update && apt install -y sqlite3
WORKDIR /astro-tablets
COPY ./src ./src
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
VOLUME /astro-tablets/output
VOLUME /astro-tablets/skyfield-data
ENV GIT_HASH=$GIT_HASH
ENTRYPOINT ["python", "./src/main.py"]
