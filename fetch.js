const fetch = require('node-fetch');

fetch("http://127.0.0.1:5000/get_birthday_data")
  .then(response => response.json())
  .then(data => {
    console.log("Birthday data:", data);
    console.log("Name:", data.name);
    console.log("Age:", data.age);
    console.log("Message:", data.message);
    console.log("Song:", data.song);
  })
  .catch(error => console.error("Error fetching data:", error));