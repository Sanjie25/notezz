
# Notezz API Reference

## Basic Setup

- Follow the setup instructions given in [READ_ME.md](https://github.com/Sanjie25/notezz/blob/main/README.md) and run the api.
- Run the api with `python run_api.py`

> The example requests in this file, will be made using the [curl](https://curl.se/download.html) command line tool.

## Setting Up Cookies file

### Issue with curl

  `curl` doesn't maintain session state between requests by default, so we'll have to use `curl`  command with a cookies file. We'll have to use both `-c`, save cookies and `-b`, send cookies flags of `curl`

#### Requests example by using a cookies file

```
# Create cookies file
touch my_cookies.txt

# Login and writing into the cookies file
curl -X POST http://127.0.0.1:12345/auth/<login/register> \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "Password123!"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

# Using the cookies file in future queries
curl -X POST http://127.0.0.1:12345/create \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "First note",
    "body": "Test content",
  }'

```

# Authentication and Administration Requests and Functions

## Registering a User

Input a json-like POST request with three fields, `username`, `password` and `role` To `http://127.0.0.1:12345/auth/login`.

```

  curl -X POST http://127.0.0.1:12345/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "example123", "role": "admin"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Login as a User

Send a POST request with fields, `username` and `password`. To `http://127.0.0.1:12345/auth/login`

```

  curl -X POST http://127.0.0.1:12345/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "example123"}' \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Logout as a User

Send an empty POST request to `http://127.0.0.1:12345/auth/login`

```

  curl -X POST http://127.0.0.1:12345/auth/logout \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Check if authorised or not

Send an empty GET request to `http://127.0.0.1:12345/auth/check-auth`

```

  curl -X GET http://127.0.0.1:12345/auth/check-auth \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## To get your profile

Send a GET request to `http://127.0.0.1:12345/auth/profile`

```

  curl -X GET http://127.0.0.1:12345/auth/profile \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt

```

## Add a collaborator (as an admin)

Send a POST request to `http://127.0.0.1/auth/add_collab`, as an admin

```

curl -X POST http://127.0.0.1:12345/auth/add_collab \
-H "Content-Type: application/json" \  
-c my_cookies.txt \  
-b my_cookies.txt \
-d '{"username": "collab_user"}'

```

# Notes Management

## Create a note

Send a POST request to `http://127.0.0.1:12345/notes/create` in json format with two fields, `title` and `body`

```

curl -X POST http://127.0.0.1:12345/notes/create \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "First Note",
    "body": "Test content"
  }'

```

## Get a Note

Send a GET request with `note_id` in url `http://127.0.0.1:12345/notes/<note_id>`.

```

curl -X DELETE http://127.0.0.1:12345/notes/1 \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \

```

## Get all notes

Send a GET request to `http://127.0.0.1:12345/notes/all`

```

curl -X GET http://127.0.0.1:12345/notes/all \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt

```

## Edit a Note

Send a PUT request with `note_id` to `http://127.0.0.1:12345/notes/<note_id>/edit` with two fields `title` and `body`.

```

curl -X PUT http://127.0.0.1:12345/notes/1/edit \
  -H "Content-Type: application/json" \
  -c my_cookies.txt \
  -b my_cookies.txt \
  -d '{
    "title": "Example text: Oh ho, you're approaching me.",
    "body": "Edited Note: "
  }'

```

## Delete a note

Send a DELETE request with `note_id` to `http://127.0.0.1:12345/notes/<note_id>/delete`.

```

curl -X DELETE http://127.0.0.1:12345/notes/1/delete \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \

```

## Delete a note using it's title

Send a DELETE request to `http://127.0.0.1:12345/notes/delete_by_title` with the field of `title` only

```

curl -X DELETE http://127.0.0.1:12345/notes/delete_by_title \
-H "Content-Type: application/json" \
-c my_cookies.txt \
-b my_cookies.txt \
-d '{"title": "note title"}'

```

# Authorisation Error due to cookies

it might look something like this,

```

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/auth/login?next=%2Fauth%2Fcheck-auth">/auth/login?next=%2Fauth%2Fcheck-auth</a>. If not, click the link.

```

in curl
