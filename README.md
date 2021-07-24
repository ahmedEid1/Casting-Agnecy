# Casting-Agnecy

## API Endpoints


## `/movies`
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

## `/actors`
