# user registration app

This app runs with the main.py module in the root dir.
main.py loads 'service' module from IdentityService package
initiates IdentityService instance and runs a script in the while loop.
Scripts enable to specify .json data file, write a new user to that file or check if the user has been registered.

For managing data, pandas and JSON libraries were used.

For the sake of simplicity, writing nested .json files was omitted.

Unit tests were performed via pytest and located in the test package.

The package for installation of this app was deployed:
python3 -m pip install test-user-auth
