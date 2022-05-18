FROM python:3.9.2

ARG project_dir=/project/

ADD requirements.txt $project_dir

WORKDIR $project_dir

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6
RUN pip install opencv-python
RUN pip install opencv-contrib-python
RUN pip install -r requirements.txt