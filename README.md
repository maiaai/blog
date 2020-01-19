# blog
This is simple Blog API endpoint developed with Django Rest_framework and Python 3.6.9
You can use this API and communicate with you front-end or connect it with some third party app. 
With this API endpoint, you can:

![Api methods](https://i.imgur.com/nehBvoD.png)
 
Additional direct publish url is added to the PostViewSet. 
Without this additional, status can be updated via PUT/PATCH request on a Post object.

As part of the API, django admin site is included.

For use of this API you need to perform next steps:

1. Create virtualenv with Python 3
2. Clone this repo
3. Install requirements: `pip install -r requirements.txt`
4. Migrate the db
    * `python manage.py migrate`. This will create default sqlite3 db that is good for testing purposes. 
For production it is recommended using Postgres
5. Create SuperUser: `python manage.py createsuperuser`
6. The root url is : "http://localhost:{port}/api/"
7. Use Postman or CURL to make requests.

NOTE: Most of the test scenarios are covered with Unit tests.

Thank you for considering me as a future coleague of yours. 