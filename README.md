# [CBIR] Project compare logo

## API request tutorial document

Main objective This project:

- Compares images, are they similar?
- Images have logo predefined

Component function:
- Add logo to do compare data 
- Delete logo in data

## I. Main API:

### I.1. Compares images, are they similar?

#### I.1.1. Request:

- URL: ``http://127.0.0.1:5000/compare``<br>
- Method: ``POST``
- Format: ``JSON``
- Input:

```json
{
  "image": "link image or image 1",
  "image": "link image or image 2"
}
```

or

```json
{
  "image": [
    "link image or image 1",
    "link image or image 2"
  ]
}
```

- Description:

```table
 Name |  Type  |               Description                  |
------|------- |--------------------------------------------|
image | string |link image or image be encoded format base64|
```

#### I.1.2. Response:

- Result:
```json
{
    "label": "coca",
    "message": "success",
    "same": true,
    "status_code": 200
}
```
- Description:
```table
    Name   |  Type  |               Description                        |
-----------|--------|--------------------------------------------------|
label      | string |name logo or null                                 |
message    | string |success or unsuccess                              |
same       | boolean|value compare same or difference logo             |
status_code| int    | status code: 200/400/500 corresponding to message|
```

### I.2. Images have logo predefined

#### I.2.1. Request:

- URL: ``http://127.0.0.1:5000/check-logo``<br>
- Method: ``POST``
- Format: ``JSON``
- Input:

```json
{
  "image": "link image",
  "label": "name label"
}
```

- Description:

```table
 Name |  Type  |               Description                  |
------|------- |--------------------------------------------|
image | string |link image or image be encoded format base64|
label | string |name logo necessary checked                 |
```


#### I.2.2. Response:


- Result:
```json
{
    "has_logo": true,
    "message": "success",
    "status_code": 200
}
```
- Description:
```table
    Name   |  Type   |               Description                                        |
-----------|---------|------------------------------------------------------------------|
has_logo   | boolean |if image have logo is true and false if not have logo, orther null|
message    | string  |success or unsuccess                                              |
status_code| int     | status code: 200/400/500 corresponding to message                |
```
## II. Other API:
### II.1 Add logo to file json

#### II.1.1. Request:

- URL: ``http://127.0.0.1:5000/add-logo``<br>
- Method: ``POST``
- Format: ``JSON``
- Input:

```json
{
  "image": "link image or image or list image",
  "label": "name label"
}
```



- Description:

```table
 Name |  Type  |               Description                  |
------|------- |--------------------------------------------|
image | string |link image or image be encoded format base64|
label | string |name label necessary add file json          |

```

#### II.1.2. Response:

- Result:
```json
{
    "add_logo": true,
    "message": "success",
    "status_code": 200
}
```
- Description:
```table
    Name   |  Type   |               Description                        |
-----------|---------|--------------------------------------------------|
add_logo   | boolean |value True if add success                         |
message    | string  |success or unsuccess                              |
status_code| int     | status code: 200/400/500 corresponding to message|
```

### II.2 Delete logo in file json

#### II.1.1. Request:

- URL: ``http://127.0.0.1:5000/delete_logo``<br>
- Method: ``POST``
- Format: ``JSON``
- Input:

```json
{
  "label": "name label necessary delete"
}
```


- Description:

```table
 Name |  Type  |               Description                  |
------|------- |--------------------------------------------|
label | string |name label necessary delete                 |
```

#### II.1.2. Response:

- Result:
```json
{
    "deleted": true,
    "message": "success",
    "status_code": 200
}
```
- Description:
```table
    Name   |  Type   |               Description                        |
-----------|---------|--------------------------------------------------|
deleted    | boolean |value True if label deleted                       |
message    | string  |success or unsuccess                              |
status_code| int     |status code: 200/400/500 corresponding to message |
```
