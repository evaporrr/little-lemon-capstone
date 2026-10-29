LITTLE LEMON - BACK-END CAPSTONE (Django REST Framework + MySQL)
================================================================

SETUP
-----
1. Create the MySQL database:
     CREATE DATABASE littlelemon CHARACTER SET utf8mb4;
2. Install dependencies:
     pip install -r requirements.txt
3. Set your MySQL credentials (defaults: user root, empty password, 127.0.0.1:3306):
     export MYSQL_DATABASE=littlelemon
     export MYSQL_USER=root
     export MYSQL_PASSWORD=your_password
4. Apply migrations and start the server:
     python manage.py migrate
     python manage.py createsuperuser      (optional, for /admin/)
     python manage.py runserver
5. Run the unit tests (the test runner creates a temporary MySQL test database):
     python manage.py test

API PATHS TO TEST (base URL http://127.0.0.1:8000)
--------------------------------------------------
Home page (static HTML served by Django)
  GET    /

User registration and authentication (Djoser)
  POST   /auth/users/                 body: {"username": "...", "password": "..."}
  POST   /auth/token/login/           body: {"username": "...", "password": "..."}
                                      -> returns {"auth_token": "<token>"}
  POST   /auth/token/logout/          header: Authorization: Token <token>
  GET    /auth/users/me/              header: Authorization: Token <token>

Menu API (GET is public; POST/PUT/PATCH/DELETE need the token header)
  GET    /menu/                       list all menu items
  POST   /menu/                       body: {"title": "Greek Salad", "price": "12.50", "inventory": 20}
  GET    /menu/<id>/                  one item
  PUT    /menu/<id>/                  full update
  PATCH  /menu/<id>/                  partial update
  DELETE /menu/<id>/                  delete

Table booking API (every request needs: Authorization: Token <token>)
  GET    /booking/tables/             list bookings
  POST   /booking/tables/             body: {"name": "Ana", "no_of_guests": 4,
                                             "booking_date": "2026-11-05T18:00:00Z"}
  GET    /booking/tables/<id>/        one booking
  PUT    /booking/tables/<id>/        full update
  PATCH  /booking/tables/<id>/        partial update
  DELETE /booking/tables/<id>/        delete

TESTING WITH INSOMNIA
---------------------
1. POST /auth/users/ to register, then POST /auth/token/login/ to get the token.
2. In Insomnia choose Auth > Bearer Token, set the prefix to "Token" and paste the token
   (or add the header  Authorization: Token <token>).
3. Call the menu and booking paths above.

PROJECT LAYOUT
--------------
LittleLemon/   project settings and root URLs
restaurant/    models (Menu, Booking), serializers, views, URLs, templates, static files, tests.py
