
document.getElementById('image').addEventListener('change', function (e){
    console.log(e.target.files[0])
})


// document.getElementById('runButton').addEventListener('click', function () {
//     fetch('/run_script', {
//         method: 'POST',
//     })
//     .then(response => response.text())
//     .then(result => {
//         document.getElementById('output').innerText = result;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }); 



function dropHandler(event) {
    event.preventDefault();

    if (event.dataTransfer.items) {
        for (var i = 0; i < event.dataTransfer.items.length; i++) {
            if (event.dataTransfer.items[i].kind === 'file') {
                console.log("lmao");
                var file = event.dataTransfer.items[i].getAsFile();
                handleFile(file);
            } else if (event.dataTransfer.items[i].kind === 'string') {
                var url = event.dataTransfer.getData('text/uri-list');
                handleURL(url);
            }
        }
    } else {
        for (var i = 0; i < event.dataTransfer.files.length; i++) {
            handleFile(event.dataTransfer.files[i]);
        }
    }
}

function dragOverHandler(event) {
    event.preventDefault();
}

function handleFileSelect(event) {
    var file = event.target.files[0];
    handleFile(file);
}

function handleFile(file) {

    var reader = new FileReader();

    reader.onload = function (e) {
        var img = new Image();
        img.src = e.target.result;

        // Do something with the image, for example, display it
        document.body.appendChild(img);
    };

    reader.readAsDataURL(file);
}

function handleURL(url) {
    fetch('/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'image_url': url }),

    })
    .then(response => response.text())
    .then(data => {
        // Handle the response from the server if needed
        console.log("data: ", data);
    })
    .catch(error => console.error('Error:', error));
}

