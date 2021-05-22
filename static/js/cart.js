var updateButton = document.getElementsByClassName('update-cart')
for(var i=0; i < updateButton.length; i++){
    updateButton[i].addEventListener('click', function(){
        var menuId = this.dataset.menu
        var action = this.dataset.action
        console.log('menuId:', menuId, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in');
        }else{
            UpdateUserOrder(menuId, action)
        }
    })
}

function UpdateUserOrder(menuId, action){
    console.log('User is logged in, sending data...')
    var url = '/update-item/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'menuId': menuId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}