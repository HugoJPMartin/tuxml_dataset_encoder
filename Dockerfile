FROM frolvlad/alpine-python-machinelearning
COPY . /app
WORKDIR /app
ENTRYPOINT ["python","-u","./linux_dataset_formatter.py"]