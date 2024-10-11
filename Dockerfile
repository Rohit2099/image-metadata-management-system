FROM python
ADD . /Assg2
WORKDIR /Assg2
RUN pip install -r requirements.txt
EXPOSE 80
EXPOSE 5000
ENTRYPOINT python app.py