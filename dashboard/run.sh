docker pull akelleh/dashboard
docker run -p 8051:8051 \
-e AWS_ACCESS_KEY_ID=`echo $AWS_ACCESS_KEY_ID` \
-e AWS_SECRET_ACCESS_KEY=`echo $AWS_SECRET_ACCESS_KEY` \
-e MYSQL_USERNAME=`echo $MYSQL_USERNAME` \
-e MYSQL_PASSWORD=`echo $MYSQL_PASSWORD` \
-e MYSQL_SERVER_ADDRESS=`echo $MYSQL_SERVER_ADDRESS` \
-e MYSQL_DATABASE=`echo $MYSQL_DATABASE` \
--network website_network \
--restart unless-stopped \
--name dashboard \
-it akelleh/dashboard 

