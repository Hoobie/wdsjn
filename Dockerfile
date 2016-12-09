FROM python:3-onbuild

COPY "data/clp/" "/usr/local/clp/"

CMD [ "python", "./rapp-wettler.py" ]
