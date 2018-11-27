#Questionnaire App Backend in Django

My first experiment with Django tech stack by building a questionnaire system that supports insertion of custom questions,
and provided endpoints to retrieve the lists, insert, delete, and also fetch specific component within the questionnaire.


## 1. Important Note
1.Make sure `PostgreSQL 11.x` is installed in your system, and in `settings.py` within `project` folder, change the `DATABASE` key accordingly.

2.If you're launching the frontend app in address other than `localhost` and/or ports other than port `3000`:

In `project/project/settings.py`, change the frontend server address accordingly in the key `CORS_ORIGIN_WHITELIST`

3.If you're launching this server app in address other than `localhost:8000`, then refer to `README` in frontend apps.

## 2. Instructions to run:
1. Install dependencies according to pipfile
2. Navigate to `project` folder (`cd project`) 
3. Run `python manage.py loaddata fixtures/questionnaire_test_data.json` to populate the database with JSON file.
4. Run `python manage.py runserver`