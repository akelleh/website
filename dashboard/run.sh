docker pull akelleh/dashboard:latest
docker run -p 8900:8900 --restart unless-stopped --link website -it akelleh/dashboard
