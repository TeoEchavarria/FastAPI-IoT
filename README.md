# FastAPI-IoT

- User CRUD.
- CRUD of things.
- API with MySQL connection.
- Visualization, monitoring and control of processes. *(Coming soon)*

## MySQL - Database structure
<p align="center"> <img src="https://user-images.githubusercontent.com/63327224/154146336-1e270c8b-ad39-4efc-9d98-754f3d6c7e64.jpg" width="350"> <img src="https://user-images.githubusercontent.com/63327224/154146638-07736fbb-5339-40c8-baa7-5d9fdc80ee1a.jpg" width="350"> </p>

### Clarifications
The values present in the *Things table,* ** **modification_dates = SET[datatime]**, is a set of all the dates on which the **Thing** has been used.

The values present in the *Users table,* ** **things = SET[thing_id]**, is a set of all UUIDs that reference the **Things** that a user has available.

## In development
An additional database will be created where the set of data that a given **Thing** has collected will be stored, then it will be analyzed and this analysis will also be stored in order to compare, and to have a temporal follow-up of the results.
The analysis will be done by means of specialized Python libraries, using methods such as Maximum Likelihood for the analysis of probabilities in stochastic processes.
