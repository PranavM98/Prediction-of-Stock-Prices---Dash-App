FROM python:3.7.3-stretch
EXPOSE 8080
# Working Directory
WORKDIR /app


# Copy source code to working directory
COPY .  /app/
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT [ "python" ] 
CMD [ "application.py" ] 