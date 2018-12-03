docker pull akelleh/website
docker run -p 8888:8888 --restart unless-stopped --network website_network --name website -it akelleh/website
