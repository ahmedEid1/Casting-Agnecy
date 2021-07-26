# Casting-Agnecy

## Motivation for project
This is an API for casting agency to allow  authenticated users to preform actions on the 
Movies and Actors data based on their Role and given permissions.


This project is the final project of Udacity full-stack nanodegree.
it's a project to practice all the skills I learned 
- Data Modeling,
- API development, documentation, and testing, 
- authentication and authorization using third party integration (authO)
- Server Deployment


## Project dependencies
- Project dependencies are listed in the requirements.txt files 
to run the project you need to have python & pip installed and run:
- `pip install -r requirments.tx`
- set the FlASK_APP env. var to flaksr
  - windows: `set FLASK_APP=flaskr`
  - linux and mac: `export FLASK_APP=flaskr`
- run the app:
  - `flask run`
  

### Database 
- add the following env variables to .env file to run the app
  - DATABASE_URL="......"
  - TEST_DATABASE_URL="......" (used for testing the app, you can the same DB for both)

### Auth0
for the auth0 to work add the following env. variables
- client_id
- client_secret
- API_AUDIENCE
- api_base_url (your auth0 domain)
- ALGORITHMS

### API
- you need to set an env variable for `login_url` which is the url to sign-in to get the token
  - if you didn't the app will work but `/login_url` will return null 

_**you can all your env. variables to a `.env` file**_

---

## Detailed instructions for scripts to install any project dependencies, and to run the development server.
TODO.......

## Documentation of RBAC controls
TODO.......

---
## RBAC controls
unauthenticated users don't have access to any of the endpoints of the API

### Roles and their permissions
- Casting Assistant
  - Can view actors and movies
  

- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
  

- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database
---

_**when a user sign up, no roles or permissions is assign to the account, 
so he still has no access to any of the endpoints.**_
- an admin need to assign roles and permissions to them


---
## API Endpoints

### (for testing) `/login_url` 
> return an url where you can sign to get a token to access endpoints in the app

> the token will be in the redirected url after you sign-in >> copy it from the url 
- you can use the following accounts to test the permissions
  - [.....................]
  - [.....................]
  - [.....................]


### `/movies`
<hr />
<details>
<summary><code>/movies</code></summary>

- Allowed methods:
  - `GET` :
    - Permission: `get:movies` 
    - Return an object with one key `movies` which is a list of all movies
    <details>
      <summary>Example:</summary>
    
      ```
          {
              "movies": [
                  {
                      "id": 1,
                      "release_date": "2021-07-22 21:36:18.800277",
                      "title": "test_movie"
                  },
                  {
                      "id": 2,
                      "release_date": "2021-07-22 21:36:39.076350",
                      "title": "test_movie"
                  },
                  {
                      "id": 3,
                      "release_date": "2021-07-22 21:36:47.650692",
                      "title": "test_movie"
                  }
              ]
          }
      ```
  
    </details> 
</details>
<hr/>

<details>
<summary><code>/movies/[int:movie_id]</code></summary>

- Allowed methods:
  - `GET` :
    - Permission: `get:movies` 
    - Return an object with one key `movie` which is the movie with the same id as in the URL
    <details>
      <summary>Example:</summary>
  
      ```
          {
              "movie": {
                  "id": 1,
                  "release_date": "2021-07-22 21:36:18.800277",
                  "title": "test_movie"
              }
          }
      ```
  
    </details> 
  <hr />
  
  - `DELETE` :
    - Permission: `delete:movies` 
    - Return an object with one key `id` after removing the movie with this is ID
    <details>
      <summary>Example:</summary>
    
        ```
            {
                "id": 1
            }
        ```
  
    </details>
  <hr />

</details>
<hr />

<details>
<summary><code>/movies/add</code></summary>

- Allowed methods:
  - `POST` :
    - Permission: `add:movies` 
    - Parameters: takes a json object with `title`, and `release_date`
    - Return an object with one key `movie` which is the new movie created
    <details>
      <summary>Example:</summary>
      
      ```
      Parameters:
          {
              "title": "new movie",
              "release_date": "2021-07-22 21:36:39.076350"
          }
      -------------------------------------------------------
      Return: 
          {
              "movie": {
                  "id": 20,
                  "release_date": "2021-07-22 21:36:39.076350",
                  "title": "new movie"
              }
          }
      ```
  
    </details> 
</details>
<hr/>

<details>
<summary><code>/movies/edit/[int:movie_id]</code></summary>

- Allowed methods:
  - `PATCH` :
    - Permission: `edit:movies` 
    - Parameters: takes a json object with optional keys `title`, and `release_date`
        - the key given get updated, and the others stay the same
    - Return an object with one key `movie` which is the movie with the given ID after updating it with the data in the request
    <details>
      <summary>Example:</summary>
      
      ```
      Parameters:
          {
              "title": "edited movie"
          }
      -------------------------------------------------------
      Return: 
          {
              "movie": {
                  "id": 20,
                  "release_date": "2021-07-22 21:36:39.076350",
                  "title": "edited movie"
              }
          }
      ```
  
    </details> 
</details>
<hr/>

### `/actors`
<hr />
<details>
<summary><code>/actors</code></summary>

- Allowed methods:
  - `GET` :
    - Permission: `get:actors` 
    - Return an object with one key `actors` which is a list of all actors
    <details>
      <summary>Example:</summary>
    
      ```
          {
            "actors": [
                {
                      "age": 5,
                      "gender": "male",
                      "id": 2,
                      "name": "test_user"
                  },
                  {
                      "age": 5,
                      "gender": "male",
                      "id": 3,
                      "name": "test_user"
                  },
                  {
                      "age": 5,
                      "gender": "male",
                      "id": 4,
                      "name": "test_user"
                  },
                  {
                      "age": 5,
                      "gender": "male",
                      "id": 5,
                      "name": "test_user"
                  }
              ]
          }
      ```
  
    </details> 
</details>
<hr/>

<details>
<summary><code>/actors/[int:actor_id]</code></summary>

- Allowed methods:
  - `GET` :
    - Permission: `get:actors` 
    - Return an object with one key `actor` which is the actor with the same id as in the URL
    <details>
      <summary>Example:</summary>
  
      ```
      Request: /actors/23
      ---------------------------------------
      Return:
          {
              "actor": {
                  "age": 5,
                  "gender": "male",
                  "id": 23,
                  "name": "test_user"
              }
          }
      ```
  
    </details> 
  <hr />
  
  - `DELETE` :
    - Permission: `delete:actors` 
    - Return an object with one key `id` after removing the actor with this is ID
    <details>
      <summary>Example:</summary>
    
      ```
      {
          "id": 23
      }
      ```
  
    </details>
  <hr />

</details>
<hr />

<details>
<summary><code>/actors/add</code></summary>

- Allowed methods:
  - `POST` :
    - Permission: `add:actors` 
    - Parameters: takes a json object with `name`, `age`, and `gender`
        - gender is male or female, and age must be greater than 0
    - Return an object with one key `actor` which is the new actor created
    <details>
      <summary>Example:</summary>
      
      ```
      Parameters:
          {
              "name": "new user",
              "age": "5",
              "gender": "male"
          }
      -------------------------------------------------------
      Return: 
          {
              "actor": {
                  "age": 5,
                  "gender": "male",
                  "id": 25,
                  "name": "new user"
              }
          }
      ```
  
    </details> 
</details>
<hr/>

<details>
<summary><code>/actors/edit/[int:actor_id]</code></summary>

- Allowed methods:
  - `PATCH` :
    - Permission: `edit:actors` 
    - Parameters: takes a json object with optional keys `name`, `age`, and `gender`
        - the key given get updated, and the others stay the same
    - Return an object with one key `actor` which is the actor with the given ID after updating it with the data in the request
    <details>
      <summary>Example:</summary>
      
      ```
      Parameters:
          {
              "name": "edited user"
          }
      -------------------------------------------------------
      Return: 
          {
              "actor": {
                  "age": 5,
                  "gender": "male",
                  "id": 25,
                  "name": "edited user"
              }
          }
      ```
  
    </details> 
</details>
<hr/>
