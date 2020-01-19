# blog
This is simple Blog API endpoint developed with Django Rest_framework and Python 3.6.9
You can use this API and communicate with you front-end or connect it with some third party app. 
With this API endpoint, you can:

![Api methods](https://i.imgur.com/nehBvoD.png)
 
Create, retrieve, update, delete (CRUD): Posts, Users and Topics.
Everyone can create user account. Post list and retrieve methods also can be performed from non-authenticated user.
In order to "Update/Delete user account, Update/Delete Post, you need to be Owner. 
Create/Update/Delete Topic" can be performed only by staff user and Post Create can be performed by authenticated user.

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