document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/get_birthday_data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("name").textContent = data.name;
            document.getElementById("age").textContent = data.age;
            document.getElementById("message").textContent = data.message;

            const audioElement = document.getElementById("song");
            audioElement.src = data.song;
            audioElement.style.display = "block";
        })
        .catch(error => console.error("Error fetching data:", error));
});