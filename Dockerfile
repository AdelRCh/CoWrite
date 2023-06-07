FROM tensorflow/tensorflow:2.10.0
WORKDIR /prod
COPY requirements_prod.txt requirements.txt
RUN pip install setuptools
RUN pip install -r requirements.txt
COPY core /core
COPY setup.py setup.py
RUN pip install .
CMD uvicorn api.fast:app --host 0.0.0.0
