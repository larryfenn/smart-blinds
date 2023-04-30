docker build -t smart-blinds:latest .
docker run --restart always --network host -d --name smart-blinds smart-blinds
