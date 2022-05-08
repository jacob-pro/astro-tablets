FROM python:3.7
ARG GIT_HASH
RUN apt update && apt install -y sqlite3
WORKDIR /astro-tablets
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src
VOLUME /astro-tablets/generated
VOLUME /astro-tablets/skyfield-data
ENV GIT_HASH=$GIT_HASH
ENTRYPOINT ["python", "./src/main.py"]
