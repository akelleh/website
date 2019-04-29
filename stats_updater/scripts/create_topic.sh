kafka-topics  \
    --create  \
    --zookeeper localhost:2181  \
    --topic stats  \
    --replication-factor 1  \
    --partitions 1