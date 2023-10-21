if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}

function count() {
    counter++;
    document.querySelector('h1').innerHTML = counter;
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;

    // runs the count function every 1000 milliseconds (1 second)
    setInterval(count, 1000);
});