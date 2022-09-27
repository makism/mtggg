FROM spark-base

# ARG spark_master_web_ui=8080

EXPOSE ${SPARK_MASTER_PORT}
EXPOSE ${SPARK_MASTER_WEBUI_PORT}
EXPOSE 6066

CMD bin/spark-class org.apache.spark.deploy.master.Master \
    --port $SPARK_MASTER_PORT \
    --webui-port $SPARK_MASTER_WEBUI_PORT \
    >> logs/spark-master.out
