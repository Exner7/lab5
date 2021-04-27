# lab5

This is a solution to the **4th voluntary exercise** introduced in
the 5th lab of the course: **Information Systems @DS-UNIPI**.

This is a Python Flask and Pymongo application service that
connects to a MongoDB database and implements basic CRUD
functionalities for the MongoDB database.

### Requirements to run the app:
1. Running **MongoDB** or a running **MongoDB docker container**.
    * A database in the MongoDB called **InfoSys**.
    * The collections **Students** and **Courses**.
        * (Optional) This [students.json](https://github.com/csymvoul/Information-Systems-Lab/blob/master/lab3-4/students.json) file can be
        used to populate the Students collection

2. Installed **Python3**, **flask** and **pymongo**.

### Testing endpoints
It is recommended to use Postman for the endpoints and requests.
The flask app is set to port 5000. So all endpoints are of the form:

    localhost:5000/endpoint

## Endpoints
---
#### GET
<br/>

*   **<code>/get-course</code>**
<br/>

    Which will accept an argument <code>courseID</code> and will return the information for the corresponding course.

---
#### POST
<br/>

*    **<code>/insert-course</code>**
<br/>

        Which will await from the user a JSON in the form of:

            {
                "name": <string>
                "courseID": <string>
                "ects": <int>
            }

        And will insert it as a course in the Courses collection, only
        if no other course with the same courseID is already exists.
<br/>
*    **<code>/insert-course-description</code>**
<br/>

        Which will accept an argument <code>courseID</code> and will add
        a description to the course with the provided courseID.
        The description is to be provided as json in the request.
        
---
