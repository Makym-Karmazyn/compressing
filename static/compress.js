console.log(123);

function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('request');
    formData.append('key1', 'value1');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => resolve(data))
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    });
}

function load_filee(event) {
    event.preventDefault(); // Зупинити стандартну поведінку

    const Form = document.querySelector('#full_form');
    const urlSearch = '/compress_or_decompress';
    const res = document.getElementById('outputText');
    console.log('test');

    RequestToServer(Form, urlSearch)
    .then(response => {
    res.innerHTML = `<p>${response.message}</p><p>Filename: ${response.filename}</p>`;
});
}