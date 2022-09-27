FROM cluster-base

ARG spark_version=3.3.0

RUN apt-get update -y && \
    apt-get install -y wget python3-dev python3-pip && \
    pip3 install wget pyspark==${spark_version}

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Copy extra libraries for Apache Spark
RUN mkdir /opt/libs/
WORKDIR /opt/libs/
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${spark_version}/hadoop-aws-${spark_version}.jar
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.9.0/aws-java-sdk-1.9.0.jar


# Copy notebooks
# ADD ["./notebooks/Template Spark.ipynb", "/opt/workspace/Template Spark.ipynb"]
# ADD ["./notebooks/schemas.py", "/opt/workspace/schemas.py"
COPY notebooks/ /opt/workspace

#
COPY src/ /app/src/mtggg
COPY scripts/ /app/scripts

ENV PYTHONPATH "${PYTHONPATH}:/app/src/"
ENV IPYTHONDIR "${SHARED_WORKSPACE}/.ipython/"

EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}

CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=
