# patelin

A Markov chain based generator for French town names.

Made using town names from [INSEE's official geographical code for January 1st 2020](https://www.insee.fr/fr/information/4316069)

# Running a container

The container needs two environment variables:

- `PATELIN_API_PORT`: the port that Gunicorn will listen to
- `PATELIN_API_WORKER`: the number of Gunicorn worker to run

# Licensing

The code for this project is licensed under the terms of the MIT license.
