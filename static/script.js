
document.getElementById('image').addEventListener('change', function (e){
    console.log(e.target.files[0])
})


async function copyToClipboard() {
    var copyText = document.querySelector("#equations");
    await navigator.clipboard.writeText(copyText.textContent);
}