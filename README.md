# Run backend and frontend to run the project
## To run the Backend use the following steps
### Please use python3 to run the following set of commands(In Command Prompt/ Terminal)
1. `cd backend`
2. To install all the required dependencies use command:- `python -m pip install -r requirements.txt`
        OR
2. if the above command doesn't works you may use `pip install -r requirements.txt`.
3. `python -m ensurepip --upgrade`.
4. To make migrations use `python manage.py makemigrations`.
5. To migrate changes use `python manage.py migrate`.
6. To run the backend server use `python manage.py runserver`.
7. open URL [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to check the running server and login using credentials _username_:`9876543210` and _password_ : `9876543210`.
8. After logging in you can see all the database tables which are used in the project.

## To run the Frontend use the following steps
### Please use python3 to run the following set of commands
1.  `cd frontend`.
2.  To install all the required dependencies use command :- `npm install`.
                             OR
2.  If the above command doesn't work use `npm i`.
3.  Then to run the frontend server use the command `npm start`.

