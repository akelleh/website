docker build -t logger .
docker run -p 8889:8889 \
-e AWS_ACCESS_KEY_ID=`echo $AWS_ACCESS_KEY_ID` \
-e AWS_SECRET_ACCESS_KEY=`echo $AWS_SECRET_ACCESS_KEY` \
--restart unless-stopped \
--network website_network \
--name logger \
-it logger
