FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim \
    git

# Project Files and Settings
ARG PROJECT=mini-ipip
ARG PROJECT_DIR=/var/www/${PROJECT}

#RUN mkdir -p $PROJECT_DIR
RUN git clone https://github.com/collab-uniba/miniIPIP_test.git $PROJECT_DIR
#COPY . $PROJECT_DIR
WORKDIR $PROJECT_DIR

# ====== #
# PYTHON #
# ====== #

# Install python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["./start.sh"]
