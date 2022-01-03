FROM python:3.9

WORKDIR /CGMdashwebapp

COPY . /CGMdashwebapp

RUN pip --no-cache-dir install --upgrade pip \
    && pip --no-cache-dir install -r requirements.txt

# EXPOSE 5000

ENTRYPOINT ["python"]
CMD [ "/CGMdashwebapp/flaskapp.py" ]
