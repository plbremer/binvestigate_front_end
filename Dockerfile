FROM continuumio/miniconda3

COPY binvestigate_gui.yml .

RUN conda env create -f binvestigate_gui.yml

RUN mkdir -p /newer_frontend/assets

RUN mkdir -p /newer_frontend/pages

RUN mkdir -p /newer_datasets/

COPY ./newer_frontend/app.py /newer_frontend/

COPY ./newer_frontend/pages/*.py /newer_frontend/pages/

COPY ./newer_frontend/assets/* /newer_frontend/assets/

COPY ./newer_datasets/* /newer_datasets/

WORKDIR /newer_frontend

EXPOSE 8050

SHELL ["conda", "run", "-n", "binvestigate_gui", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "binvestigate_gui", "python", "./app.py"]


