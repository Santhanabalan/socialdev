let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    let formData = {
        'username':form.username.value,
        'password':form.password.value,
    }
    fetch('http://localhost:8000/api/users/token/',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Token',data.access)
        if (data.access){
            localStorage.setItem('token', data.access)
            window.location = 'http://localhost:5500/frontend/projects-list.html'
        }
        else{
            alert('Username or Password is incorrect')
        }
    })
})