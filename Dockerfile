# Starting from base miniconda image
FROM continuumio/miniconda3# Setting working directory in destination
WORKDIR /app# This is the complete set of libraries required
RUN conda install -c pyviz holoviz
RUN conda install -c pyviz geoviews-core
RUN conda install geopandas# Copy the relevant folder into the container
COPY ./dep-test/ .# Run panel serve to start the app
CMD panel serve --address="0.0.0.0" --port=$PORT Dashboard.ipynb --allow-websocket-origin=[].herokuapp.com