FROM python:3.7-buster
ADD . /vk
WORKDIR /vk
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "/vk/main.py" ]