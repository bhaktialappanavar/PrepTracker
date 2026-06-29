
const text = "Welcome Back!";

let index = 0;

function typeEffect() {

    if(index < text.length){

        document.getElementById("typing").innerHTML += text.charAt(index);

        index++;

        setTimeout(typeEffect,100);

    }

}

typeEffect();

