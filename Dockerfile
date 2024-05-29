    FROM python:3.9-slim-bullseye
    ENV HOME /home

    WORKDIR ${HOME}
    ENV PYTHONPATH ${HOME}

    COPY . .

    RUN apt-get update && apt-get install -y gcc \
    && apt-get install -y libgl1-mesa-glx libglib2.0-0

    RUN pip3 install -r requirements.txt    

    RUN python3 -m nltk.downloader stopwords


    EXPOSE 5000

    CMD ["python3", "app/api.py"]

    
    


