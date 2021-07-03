# BLB

Entry project for BLB ventures Dango + Graphene social media app.

## Execute

All graphQl queries can be executed in `http://localhost:8000/graphql`. To run the server use the command:

`python manage.py runserver`

## TODO

- Move queries from main schema to apps
- Fix issue where admin portal cache authentication, overrides JWT token auth. 
- Add tests
- Treat all raised errors during qraphql queries equally