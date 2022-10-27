FROM python:3.8-buster
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
WORKDIR /app
COPY requirements.txt .
COPY *.py /app/
COPY *.sh /app/
RUN pip --no-cache-dir install -r requirements.txt
CMD ['run.sh']