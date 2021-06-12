# Install Python
FROM python:3.6 as api
RUN apt-get -y update && apt-get install -y libzbar-dev
RUN apt-get update && apt-get install -y --no-install-recommends nano sudo iputils-ping && rm -rf /var/lib/apt/lists/*

# Create folder code and copy all files
RUN mkdir /home/lifco
ADD requirements.txt /home/lifco
ADD . /home/lifco
WORKDIR /home/lifco
RUN ls -al
# Install Python
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt