FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime
# Install some basic utilities


# Installing requirements for GUI
RUN apt-get -y update
RUN apt-get install -y --fix-missing  cmake
RUN apt-get install -y libgl1-mesa-glx
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
RUN apt-get install -y ttf-mscorefonts-installer

# Extra libraries needed
RUN conda install -c conda-forge scipy
RUN conda install -c anaconda pyqt

# Make keyboard work
RUN apt-get install -y libxkbcommon-dev
RUN apt-get install -y libxcb-xkb-dev
RUN apt-get install -y libxslt1-dev

# Chat-gpt stuff
RUN apt-get update && apt-get install -y \
    qt5-default \
    && rm -rf /var/lib/apt/lists/*

# Stable Diffusion stuff
RUN pip install \
    diffusers==0.7.2 \
    transformers==4.24.0 \
    accelerate==0.14.0 

# Copy program and set working dir
COPY gui.py /app/
WORKDIR /app/

CMD [ "python", "./gui.py"]
