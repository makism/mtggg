# ARG debian_buster_image_tag=8-jre-slim
FROM openjdk:8-jre-slim

ARG shared_workspace=/opt/workspace
RUN mkdir -p ${shared_workspace}

RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y libpq-dev libsasl2-dev && \    
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SHARED_WORKSPACE=${shared_workspace}

VOLUME ${shared_workspace}
CMD ["bash"]
