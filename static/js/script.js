var pass = document.getElementById("password");
var message = document.getElementById("message");
var requirements = {
    letter  : /[a-z]/g,
    capital : /[A-Z]/g,
    number  : /[0-9]/g,
    length  : 8
};

pass.onfocus = function() {
    document.getElementById("message").style.display = "block";
}

pass.onblur = function() {
    document.getElementById("message").style.display = "none";
}

pass.onkeyup = function() {
    validateRequirements(pass.value.match(requirements.letter), "letter");
    validateRequirements(pass.value.match(requirements.capital), "capital");
    validateRequirements(pass.value.match(requirements.number), "number");
    validateRequirements(pass.value.length >= requirements.length, "length");
}

function validateRequirements(isValid, id) {
    var element = document.getElementById(id);
    if(isValid) {
        element.classList.remove("invalid");
        element.classList.add("valid");
    } else {
        element.classList.remove("valid");
        element.classList.add("invalid");
    }
}