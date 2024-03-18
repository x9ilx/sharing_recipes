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
echo 'START CREATE SUPER USER FOR REVIEWER'
echo '------------------------------------------------'
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(email='admin@admin.com').exists():
    user=User.objects.create_user('admin', password='admin')
    user.is_superuser = True
    user.is_staff = True
    user.email = 'admin@admin.com'
    user.first_name = 'admin'
    user.last_name = 'admin'
    user.save()
    print(f'User: "login: admin, email: admin@admin.com, password: admin" created')
else:
    print(f'User: "login: admin, email: admin@admin.com, password: admin" exists')
exit()
EOF
echo '------------------------------------------------'
echo 'END CREATE SUPER USER FOR REVIEWER'
echo '------------------------------------------------'


echo '------------------------------------------------'
echo 'RUN SERVER'
echo '------------------------------------------------'
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi
