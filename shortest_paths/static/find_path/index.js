'use strict';
let a = {};
document.addEventListener('DOMContentLoaded', ()=>{

    document.querySelector('#submit').onclick = () => {
        // Initialize new Ajax request
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/api/getpath/');
        console.log("update");
        request.onload = () =>{
            const data = JSON.parse(JSON.parse(request.responseText));
            a = data;
            console.log(`data: ${data}`)
            console.log(`typeof data: ${typeof(data)}`)
            document.querySelector('#dist').innerHTML = data['dist'];
            document.querySelector('#path').innerHTML = data['path'];
        }

        // const data = new FormData();
        // data.append('choice', document.querySelector('#choice'));
        let data = JSON.stringify({'source': document.querySelector('#source').value,
                                    'dest': document.querySelector('#dest').value})
        request.send(data);
    }
});