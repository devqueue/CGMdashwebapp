docker build -t cgmdashboard:latest .
docker run -p 8050:5000 -it cgmdashboard
# heroku turn on or off
heroku maintenance:on --app cgmdashboard