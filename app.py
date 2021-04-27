# Import necessary modules
from flask import Flask, jsonify, request, Response
from pymongo import MongoClient


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
        return Response( 'Improper request arguments.', status = 400, mimetype = 'application/json' )
    
    # retreive course from database
    course = courses.find_one( { 'courseID': course_id } )
    
    # initialize output
    output = None

    # if course found construct output as JSON
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


# ... Endpoints Declarations End



# Run the flask app
if __name__ == '__main__':
    app.run( debug = True, host = '0.0.0.0', port = 5000 )
