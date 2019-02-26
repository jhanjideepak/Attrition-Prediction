sudo service nginx start &
gunicorn --chdir /home/howathon/api/ --config gunicorn.cfg views:app