FROM tensorflow/tensorflow:2.10.0
# OR for apple silicon, use this base image instead
# FROM armswdev/tensorflow-arm-neoverse:r22.09-tf-2.10.0-eigen
WORKDIR /prod
# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY taxifare taxifare
COPY requirements_prod.txt requirements.txt
RUN pip install -r requirements.txt
COPY setup.py setup.py
RUN pip install .
# COPY Makefile Makefile
# RUN make reset_local_files
CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
