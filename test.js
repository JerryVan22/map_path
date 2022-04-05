async function printJSON() {
    const response = await fetch("http://localhost:8000/data.json");
    const json = await response.json();
    alert(json['err'])
}

printJSON();
alert('hello')
