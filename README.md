# timeclock
The project consists of building a simple application serving a GraphQL API for
employees to clock in and out, and also for them to check the number of hours worked
today, on the current week, and on the current month.


## Instructions to run locally
* ``git clone git@github.com:nahidsaikat/timeclock.git``
* ``cd timeclock``
* ``virtualenv .venv``
* ``source .venv/bin/activate``
* ``pip install -r requirements.txt``
* ``python manage.py migrate``
* ``python manage.py runserver``
* Visit ``http://localhost:8000/graphql``
* Run test ``python manage.py test``

## Some Images
![Alt text](images/timeclock1.png?raw=true "Title")
![Alt text](images/timeclock2.png?raw=true "Title")
![Alt text](images/timeclock3.png?raw=true "Title")
![Alt text](images/timeclock4.png?raw=true "Title")
