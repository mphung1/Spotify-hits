# Starting from base miniconda image
FROM continuumio/miniconda3
WORKDIR /app
COPY requirements.txt .
RUN conda install --r requirements.txt
COPY . .
CMD panel serve --address="0.0.0.0" --port=$PORT Dashboard.ipynb --allow-websocket-origin=hit-playah.herokuapp.com