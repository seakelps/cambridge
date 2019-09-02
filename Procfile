# heroku config:set DISABLE_COLLECTSTATIC=1
release: python manage.py migrate
web: npm run build_release && python manage.py collectstatic --noinput && gunicorn citycouncil.wsgi --log-file -
