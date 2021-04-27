# Import necessary modules
from flask import Flask

# Initialize the flask app
app = Flask( __name__ )



# Endpoints Declarations Start ...


# test endpoint
@app.route( '/' )
def test():
    return "Test successful"


# ... Endpoints Declarations End



# Run the flask app
if __name__ == '__main__':
    app.run( debug = True, host = '0.0.0.0', port = 5000 )