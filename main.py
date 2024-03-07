from website import create_app
# \website is a python package because it has a __init__.py file
# when imported, the __init__.py file will run

developer_mode = False

app = create_app()

if __name__ == '__main__':
    # __name__ is the name of the file that is running
    # this if statement will only return true if this file is run directly
    # not when it is run by being imported by another file
    # which would activate the website when we do not want it to
    app.run(debug=developer_mode)