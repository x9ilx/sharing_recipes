echo '------------------------------------------------'
echo 'START MIGRATIONS'
echo '------------------------------------------------'
python manage.py migrate
echo '------------------------------------------------'
echo 'END MIGRATION'
echo '------------------------------------------------'


echo '------------------------------------------------'
echo 'START COLLECT STATIC'
echo '------------------------------------------------'
python manage.py collectstatic --noinput
cp -r /app/collected_static/. /static/static/
echo '------------------------------------------------'
echo 'END COLLECT STATIC'
echo '------------------------------------------------'


echo '------------------------------------------------'
echo 'START LOAD BASE DATA'
echo '------------------------------------------------'
python manage.py loadbasedata
echo '------------------------------------------------'
echo 'END LOAD BASE DATA'
echo '------------------------------------------------'


echo '------------------------------------------------'
echo 'RUN SERVER'
echo '------------------------------------------------'
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi
