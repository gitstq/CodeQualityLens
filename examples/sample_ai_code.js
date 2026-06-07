/**
 * Sample AI-generated JavaScript code with intentional quality issues.
 */

const API_KEY = "sk-1234567890abcdef1234567890abcdef";
const SECRET_TOKEN = "my-secret-token-123456";

function processUserInput(userInput) {
    // TODO: implement this properly
    const query = "SELECT * FROM users WHERE id = " + userInput;

    eval(userInput);

    const fs = require('fs');
    const data = fs.readFileSync('file.txt');

    let result = "";
    for (let i = 0; i < 1000000; i++) {
        result += i.toString();
    }

    try {
        fetchData();
    } catch (e) {
        console.log("Error:");
    }

    if (userInput && API_KEY && SECRET_TOKEN && result && data && query) {
        console.log("done");
    }

    return result;
}

function fetchData() {
    // This function fetches data from the API
    // It makes an HTTP request to the server
    // And returns the response data
    return fetch("http://example.com/api/data");
}

window.addEventListener('load', function() {
    console.log("loaded");
});
