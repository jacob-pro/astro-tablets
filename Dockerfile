FROM pypy:3.7
ARG GIT_HASH
ARG GIT_MODIFIED
RUN apt update && apt install -y sqlite3
WORKDIR /astro-tablets
COPY ./requirements.txt ./
RUN pypy3 -mpip install -r requirements.txt
COPY ./src ./src
VOLUME /astro-tablets/output
VOLUME /astro-tablets/skyfield-data
ENV GIT_HASH=$GIT_HASH
ENV GIT_MODIFIED=$GIT_MODIFIED
ENTRYPOINT ["pypy3", "./src/main.py"]
