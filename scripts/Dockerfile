FROM ubuntu:20.04

LABEL authors="Daniel Lopez <daniellopez@nevada.unr.edu>"

# set up deps for blender
RUN apt-get update && \
	apt-get install -y \
		curl \
		libfreetype6 \
		libglu1-mesa \
		libxi6 \
		libxrender1 \
		xz-utils && \
	apt-get -y autoremove

# Download blender
ENV BLENDER_MAJOR 2.82
ENV BLENDER_VERSION 2.82a
ENV BLENDER_URL https://download.blender.org/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux64.tar.xz

RUN curl -L ${BLENDER_URL} | tar -xJ -C /usr/local/ \
    && mv /usr/local/blender-${BLENDER_VERSION}-linux64 /usr/local/blender

# run the pip install for the bundled python
# todo move the copy common to earlier, and add requirements.txt and change line 29
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && ls /usr/local/blender/${BLENDER_MAJOR}/python/lib \
    && /usr/local/blender/${BLENDER_MAJOR}/python/bin/python3.7m get-pip.py \
    && /usr/local/blender/${BLENDER_MAJOR}/python/bin/python3.7m -m pip install pyyaml yamale --user

# Get the config common library near the blender executable
COPY common.py /usr/local/blender/${BLENDER_MAJOR}/python/lib/python3.7/

VOLUME /media
WORKDIR /
ENTRYPOINT ["/usr/local/blender/blender", "-b"]