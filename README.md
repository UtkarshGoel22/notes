# Secure and Scalable RESTful APIs for Notes Management

## Welcome! 👋

Thanks for checking out this repository.
This is a secure and scalable RESTful APIs to manage notes. The APIs enable users to perform CRUD operations on notes, share them with others, and search based on keywords. The project is implemented using Flask, incorporating features such as secure authentication, rate limiting, and search functionality.

## Table of contents

-[Local Setup](#local-setup)

- [Technical Details](#technical-details)
  - [Framework](#framework:-flask)
  - [Database](#database:-mongodb)
  - [Rate Limiting](#rate-limiting:-flask-limiter)
  - [Authentication](#authentication:-argon2-cffi-and-pyjwt)
  - [Search](#search-functionality:-text-indexing)
- [Endpoints](#endpoints)
  - [User signup](#1.-post-/api/auth/signup)
  - [User signin](#2.-post-/api/auth/signin)
  - [Create note](#3.-post-/api/notes)
  - [Get notes](#4.-get-/api/notes)
  - [Get note](#5.-get-/api/notes/<note_id>)
  - [Delete note](#6.-delete-/api/notes/<note_id>)
  - [Update note](#7.-put-/api/notes/<note_id>)
  - [Share note](#8.-post-/api/notes/<note_id>/share)
  - [Search note](#9.-get-/api/search?q=<query>)

## Local Setup

1. Install docker desktop.
2. Open the docker desktop
3. Start the docker container.

```shell
docker-compose up -d
```

4. Go to run.py file and add the host in the update statement.

```
app.run(debug=True, load_dotenv=True, port=os.environ.get("PORT"), host="0.0.0.0")
```

5. Create indexes only once during the initial setup. Make sure that the container is running in the background. Skip if already created index.

```shell
python create-index.py
```

6. Local setup is complete now you can test the APIs.

## Technical Details

### Framework: Flask

Flask has been used due to its simplicity, flexibility, and vibrant ecosystem. Its lightweight and minimalistic design allows it to kickstart development quickly while maintaining a high level of customization. It has extensive community support and well-structured documentation which facilitates rapid development.

### Database: MongoDB

MongoDB is selected as the database to store notes data. It offers ACID compliance, extensibility, and support for complex queries, making it suitable for the requirements of this project. Its flexible schema allows it to adapt to changes easily, and its scalability ensures that the system can grow as needed.

### Rate Limiting: Flask-Limiter

To handle high traffic and prevent abuse, the flask-limiter package is employed. This tool allows for easy implementation of rate limiting and request throttling, ensuring the API remains responsive and secure.

### Authentication: argon2-cffi and PyJWT

For security, the project uses argon2id for hashing user passwords and a JWT (JSON Web Token) authentication mechanism. Argon2id provides a robust and flexible solution for securely hashing passwords, helping to safeguard user accounts and enhance overall system security.

### Search Functionality: Text Indexing

To enhance search performance, text indexing is implemented. MongoDB allows the use of compound indexes for search. This feature enables users to search for notes based on keywords efficiently.

## Endpoints

### 1. POST /api/auth/signup

- This endpoint is invoked whenever a user tries to sign up on the platform.
- Check if the user with the given username already exists.
- Hashes the password.
- Creates new users.

**Generic Payload**:
{
"first_name": <string> <A-Z letters and non-consecutive apostrophes(') and/or dashes(-)>,
"last_name": <string> <A-Z letters and non-consecutive apostrophes(') and/or dashes(-)>,
"username": <string> <Valid email address>,
"password": <string> <Alphanumeric with at least 1 special character and having min length of 6>,
}

**Example Curl**

```shell
curl --location --request POST 'http://localhost:3000/api/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "john@email.com",
    "password": "notes@123"
}'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "user_id": <Document id of the user>,
    },
    "message": "User created successfully.",
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

### 2. POST /api/auth/signin

- This endpoint is invoked whenever a user tries to sign in on the platform.
- Check if the user with the given username exists.
- Verifies the password.
- Generates and returns a JWT token.

**Generic Payload**:

```
{
    "username": <string> <Valid email address>,
    "password": <string> <Alphanumeric with at least 1 special character and having min length of 6>,
}
```

**Example Curl**

```shell
curl --location --request POST 'http://localhost:3000/api/auth/signin' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "john@email.com",
    "password": "password@123"
}'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "access_token": <JWT token>,
    },
    "message": "User logged in successfully.",
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

### 3. POST /api/notes

- This endpoint is invoked whenever a user tries to create a new note.
- Creates new note document.
- Appends the note object ID in the notes field in the user document.

**Generic Payload**:

```
{
    "body": <string>,
    "title": <string>,
}
```

**Example Curl**

```shell
curl --location --request POST 'http://localhost:3000/api/notes' \
--header 'Authorization: Bearer <Access Token>' \
--header 'Content-Type: application/json' \
--data '{
    "body": "Note body.",
    "title": "Note title."
}'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "note_id": <Note document id>
    },
    "message": "Note created successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```

{
"data": {},
"message": "Unauthorized access.",
}

```

### 4. GET /api/notes

- This endpoint is invoked whenever a user tries to fetch a list of all of his notes.

**Example Curl**

```shell
curl --location --request GET 'http://localhost:3000/api/notes' \
--header 'Authorization: Bearer <Access Token>'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "notes": [
            {
                "_createdAt": "2024-03-23T16:38:33.742000",
                "_id": "65ff0589649e456940a94ed7",
                "_lastModifiedAt": "2024-03-23T16:38:33.742000",
                "author": "65ff04a403c46e4bed5faa59",
                "body": "Note body",
                "title": "Note title"
            }
        ]
    },
    "message": "Note(s) fetched successfully."
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```

### 5. GET /api/notes/<note_id>

- This endpoint is invoked whenever a user tries to fetch a particular note.
- Checks whether the user has read access to the note.

**Example Curl**

```shell
curl --location --request GET 'http://localhost:3000/api/notes/<note_id>' \
--header 'Authorization: Bearer <Access Token>'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "notes": [
            {
                "_createdAt": "2024-03-23T16:38:33.742000",
                "_id": "65ff0589649e456940a94ed7",
                "_lastModifiedAt": "2024-03-23T16:38:33.742000",
                "author": "65ff04a403c46e4bed5faa59",
                "body": "Note body",
                "title": "Note title"
            }
        ]
    },
    "message": "Note(s) fetched successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```

### 6. DELETE /api/notes/<note_id>

- This endpoint is invoked when the user tries to delete a note.
- Checks if the note exists.
- Checks whether the user has access to the note.
- Deletes the note.

**Example Curl**

```shell
curl --location --request DELETE 'http://localhost:3000/api/notes/<note_id>' \
--header 'Authorization: Bearer <Access Token>'
```

**Returns**

- Case Success: 200

```
{
    "data": {},
    "message": "Note deleted successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```

### 7. PUT /api/notes/<note_id>

- This endpoint is invoked when the user tries to update a note.
- Checks if the note exists.
- Checks whether the user has access to the note.
- Updates the note.

**Generic Payload**:
{
"body": <string> <at least one of the body or title should be present in the payload>,
"title": <string>,
}

**Example Curl**

```shell
curl --location --request PUT 'http://localhost:3000/api/notes/<note_id>' \
--header 'Authorization: Bearer <Access Token>' \
--header 'Content-Type: application/json' \
--data '{
    "body": "Note body",
    "title": "Note title"
}'
```

**Returns**

- Case Success: 200

```
{
    "data": {},
    "message": "Note updated successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```

### 8. POST /api/notes/<note_id>/share

- This endpoint is invoked when the user tries to share a note.
- Checks if the note exists.
- Checks whether the user has write access to the note.
- Checks if a user is trying to share the note to himself.
- Check if the note is already shared.
- Shares the note with another user.

**Generic Payload**:
{
"share_with": <string> <email of the user the note needs to be shared with>
}

**Example Curl**

```shell
curl --location --request POST 'http://localhost:3000/api/notes/<note_id>/share' \
--header 'Authorization: Bearer <Access Token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "share_with": "doe@email.com"
}'
```

**Returns**

- Case Success: 200

```
{
    "data": {},
    "message": "Note shared successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```

### 9. GET /api/search?q=<query>

- This endpoint is invoked when the user tries to search for notes.
- Searches for notes based on the keywords provided.

**Example Curl**

```shell
curl --location --request GET 'http://localhost:3000/api/search?q=<query>' \
--header 'Authorization: Bearer <Access Token>'
```

**Returns**

- Case Success: 200

```
{
    "data": {
        "notes": [
            {
                "_createdAt": "2024-03-23T16:38:33.742000",
                "_id": "65ff0589649e456940a94ed7",
                "_lastModifiedAt": "2024-03-23T16:47:38.417000",
                "author": "65ff04a403c46e4bed5faa59",
                "body": "Note body",
                "title": "Note title",
            }
        ]
    },
    "message": "Note(s) fetched successfully."
}
```

- Case Failure: 400

```
{
    "data": {},
    "errors": <error details>,  (optional)
    "message": <error message>,
}
```

- Case Failure: 401

```
{
    "data": {},
    "message": "Unauthorized access.",
}
```
