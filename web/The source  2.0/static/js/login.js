function login() {
    const secret_username = "kidz";
    const secret_password = "kidz_3@sy_$1mple";

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if(secret_password == password && username == secret_username)
    {
        window.location.replace("{{ url_for('reveal') }}");
    } else {
        alert('Incorrect username or password');
    }
}