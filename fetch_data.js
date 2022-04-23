async function printJSON(markerLayer) {
    // alert('ok')
    const response = await fetch("./data/place.json");
    var sel_destination = document.getElementById("destination");
    var sel_place_of_departure = document.getElementById("place_of_departure")


    const json = await response.json();
    // alert(json.length)
    for (i = 0; i < json.length; i++) {
        var opt = document.createElement("option");
        opt.value = json[i]["id"];
        opt.text = json[i]["name"];
        sel_destination.add(opt, null);

        var opt2 = document.createElement("option");
        opt2.value = json[i]["id"];
        opt2.text = json[i]["name"];
        sel_place_of_departure.add(opt2, null)


        //console.log(json[i]["id"])
        markerLayer.add([{
            "id": json[i]["id"],   //点标记唯一标识，后续如果有删除、修改位置等操作，都需要此id
            "styleId": json[i]["styleId"],  //指定样式id
            "position": new TMap.LatLng(json[i]["position"][0], json[i]["position"][1]),  //点标记坐标位置
        }
        ])
    }
}