FROM python:3.11-slim

# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1

# Creating working directory
WORKDIR /usr/src/Maxwell_bot

# Copy content
COPY . .

# Installing dependencies
RUN pip3 install -r ./requirements.txt

# Running the app
ENTRYPOINT ["sh", "entry.sh"]
