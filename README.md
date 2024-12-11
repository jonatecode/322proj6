[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/pTO8UJvB)
# Project 6: Brevet time calculator service

Simple listing service from project 5 stored in MongoDB database.

### Author: Jon Ng, jonn@uoregon.edu

## What is in this repository

You have a minimal implementation of Docker compose in DockerRestAPI folder, using which you can create REST API-based services (as demonstrated in class).

## Recap

You will reuse *your* code from Project 5. Recall: you created the following functionalities in Project 5's `DockerMongo` directory:

1. Two buttons ("Submit") and ("Display") in the page where you have controle times.
2. On clicking the Submit button, the control times were be entered into the database.
3. On clicking the Display button, the entries from the database were be displayed in a new page.
4. You also handled error cases appropriately.
5. REST API to provide endpoints to retrieve brevet control times stored in MongoDB
6. Consumer Programs REST API with Python

## Functionality

This project integrates the the following four parts.
1.
   * `http://<host:port>/listAll` should return all open and close times in the database
   * `http://<host:port>/listOpenOnly` should return open times only
   * `http://<host:port>/listCloseOnly` should return close times only
2. 
   * `http://<host:port>/listAll/csv` should return all open and close times in CSV format
   * `http://<host:port>/listOpenOnly/csv` should return open times only in CSV format
   * `http://<host:port>/listCloseOnly/csv` should return close times only in CSV format
   * `http://<host:port>/listAll/json` should return all open and close times in JSON format
   * `http://<host:port>/listOpenOnly/json` should return open times only in JSON format
   * `http://<host:port>/listCloseOnly/json` should return close times only in JSON format
3. 
   * `http://<host:port>/listOpenOnly/csv?top=3` should return top 3 open times only (in ascending order) in CSV format
   * `http://<host:port>/listOpenOnly/json?top=5` should return top 5 open times only (in ascending order) in JSON format
   * `http://<host:port>/listCloseOnly/csv?top=6` should return top 5 close times only (in ascending order) in CSV format
   * `http://<host:port>/listCloseOnly/json?top=4` should return top 4 close times only (in ascending order) in JSON format
4. 
Consumer programs (using Python `requests`, PHP or JQuery) to use the service that you expose. The `website` directory inside `DockerRestAPI` provides a PHP example for a different API and other examples were given in lecture. The Python `requests` approach is probably the simplest choice for the client portion. ([REST examples](https://github.com/UO-CS322/cs322-f24/tree/main/week9) from lecture.)

## How to Use
1. Clone Repositiory
2. Run with Docker Compose
3. Populate the Database
4. Test the Endpoints
5. Run Test Cases

