# Import necessary modules
from flask import Flask, jsonify
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


# test endpoint
@app.route( '/' )
def test():
    course = courses.find_one( {} )
    output = {
        'name': course[ 'name' ],
        'courseID': course[ 'courseID' ],
        'ects': course[ 'ects' ]
    }
    return jsonify( output )


# ... Endpoints Declarations End



# Run the flask app
if __name__ == '__main__':
    app.run( debug = True, host = '0.0.0.0', port = 5000 )
