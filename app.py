# Import necessary modules
from flask import Flask, jsonify, request, Response
from pymongo import MongoClient

import json


# Initialize the flask app
app = Flask( __name__ )


# Initialize the mongo client object
client = MongoClient( 'mongodb://localhost:27017' )

# Select the databse InfoSys
db = client[ 'InfoSys' ]

# Select the Courses collection
courses = db[ 'Courses' ]

# Select the Students collection
students = db[ 'Students' ]



# Endpoints Declarations Start ...


# [ GET ] ( endpoint ): /get-course
#
# Which will accept courseID as an argument and will
# return the information for the corresponding course.
@app.route( '/get-course', methods = [ 'GET' ] )
def get_course():

    # get the courseID argument
    course_id = request.args.get( 'courseID' )
    
    # if course_id is empty return with an error response
    if not course_id:
        return Response( 'Improper request arguments.', status = 500, mimetype = 'application/json' )
    
    # retreive course from database
    course = courses.find_one( { 'courseID': course_id } )
    
    # initialize output
    output = None

    # if course found construct output as json
    if course:
        output = {
            'name': course[ 'name' ],
            'courseID': course[ 'courseID' ],
            'ects': course[ 'ects' ]
        }
    
        # if the course has a description add it to output
        if 'description' in course:
            output[ 'description' ] = course[ 'description' ]
    
    return jsonify( output )


# [POST] ( endpoint ): /insert-course
#
# Which will await a json from the user with the keys below:
# 'name', 'courseID' and 'ects'.
# And will insert it as a course in the Courses collection.
@app.route( '/insert-course', methods = [ 'POST' ] )
def insert_course():
    
    # initialize the request data object
    data = None
    
    try:
        # retrieve the request json data
        data = json.loads( request.data )
    except Exception as e:
        # if an exception occurs return with an error response
        return Response( 'Bad JSON content', status = 500, mimetype = 'application/json' )
    
    # if data doesn't contain required keys return with an error response
    if 'name' not in data or 'courseID' not in data or 'ects' not in data:
        return Response( 'Improper request data', status = 500, mimetype = 'application/json' )
    
    # if a course with courseID is already present in the courses collection
    if ( courses.find( { 'courseID': data[ 'courseID' ] } ).count() != 0 ):
        # return with a Response message
        return Response( 'Given course already exists.', status = 200, mimetype = 'application/json' )

    # construct course to be inserted
    course = {
        'name': data[ 'name' ],
        'courseID': data[ 'courseID' ],
        'ects': data[ 'ects' ]
    }

    # insert course
    courses.insert_one( course )
    
    # return with a success response
    return Response( 'New course inserted successfully.', status = 200, mimetype = 'application/json' )


# [ POST ] ( endpoint ): /insert-course-description
#
# Which will accept an argument courseID and will add
# a description to the course with the provided courseID.
# The description is to be provided as json in the request.
@app.route( '/insert-course-description', methods = [ 'POST' ] )
def insert_course_description():

    # get the courseID argument
    course_id = request.args.get( 'courseID' )
    
    # if course_id is empty return with an error response
    if not course_id:
        return Response( 'Improper request arguments.', status = 500, mimetype = 'application/json' )
    
    # retreive course from database
    course = courses.find_one( { 'courseID': course_id } )

    # if the course does not exist return with an error response
    if not course:
        return Response( 'The course does not exist.', status = 500, mimetype = 'application/json' )
    
    # initialize the request data object
    data = None

    try:
        # retrieve the request json data
        data = json.loads( request.data )
    except Exception as e:
        # if an exception occurs return with an error response
        return Response( 'Bad JSON content', status = 500, mimetype = 'application/json' )
    
    # if data doesn't contain required description key return with an error response
    if 'description' not in data:
        return Response( 'Improper request arguments.', status = 500, mimetype = 'application/json' )
    
    # update the course with the description
    courses.update_one( { 'courseID': course_id }, { '$set': { 'description': data[ 'description' ] } } )

    return Response( 'Description added to course.', status = 200, mimetype = 'application/json' )


# [ PUT ] ( endpoint ): /add-course/<string:email>
#
# Receives a courseID in the request body (as JSON) and adds the corresponding
# course to the student with the provided email in an array field called courses.
@app.route( '/add-course/<string:email>', methods = [ 'PUT' ] )
def add_course( email ):

    # initialize the request data object
    data = None

    try:
        # retrieve the request json data
        data = json.loads( request.data )
    except Exception as e:
        # if an exception occurs return with an error response
        return Response( 'Bad JSON content', status = 500, mimetype = 'application/json' )
    
    # if courseID not in request data return with an error response
    if 'courseID' not in data:
        return Response( 'Improper request data', status = 500, mimetype = 'application/json' )
    
    # find the student with the provided email
    student = students.find_one( { 'email': email } )

    # if the student is not found return with an error response
    if not student:
        return Response( 'No student found.', status = 500, mimetype = 'application/json' )
    
    # find the corresponding course
    course = courses.find_one( { 'courseID': data[ 'courseID' ] } )
    
    # if the course does not exists return with an error response
    if not course:
        return Response( 'The course does not exist.', status = 500, mimetype = 'application/json' )
    
    # ( optional ) to not include the ObjectId
    # del course[ '_id' ]

    # add the course to the student's courses
    students.update_one( { 'email': email }, { '$addToSet': { 'courses': course } } )

    # return with a success response
    return Response( 'Course added to student\'s courses.', status = 200, mimetype = 'application/json' )



# ... Endpoints Declarations End



# Run the flask app
if __name__ == '__main__':
    app.run( debug = True, host = '0.0.0.0', port = 5000 )
