FROM python:3.10

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# setup files
COPY . /app
WORKDIR /app

# update pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt


CMD ["python", "HoneygainBot.py", "true"]
