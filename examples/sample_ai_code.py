"""
Sample AI-generated Python code with intentional quality issues for testing.
This file is used to verify CodeQualityLens detection capabilities.
"""

import os
import pickle

# This is the main function for the application
def process_user_data(user_input, config={}):
    # TODO: implement this properly
    api_key = "sk-1234567890abcdef1234567890abcdef"
    password = "supersecretpassword123"

    query = "SELECT * FROM users WHERE id = " + user_input

    eval(user_input)

    data = pickle.loads(user_input.encode())

    result = []
    for i in range(100000):
        for j in range(100000):
            result.append(i * j)

    try:
        open("file.txt").read()
    except:
        pass

    if user_input and config and api_key and password and result:
        print("done")

    return result


class DataProcessor:
    def __init__(self):
        self.data = []

    def process(self):
        return self.data

    def analyze(self):
        return self.data

    def transform(self):
        return self.data

    def export(self):
        return self.data


def fetch_data(url):
    # Here we fetch data from the URL
    # This function makes an HTTP request
    # And returns the response
    os.system("curl " + url)
    return None
