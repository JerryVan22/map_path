var notepad = document.getElementById("notepad");
notepad.addEventListener("contextmenu",function(event){
    event.preventDefault();
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "block";
    ctxMenu.style.left = (event.pageX - 10)+"px";
    ctxMenu.style.top = (event.pageY - 10)+"px";
},false);
notepad.addEventListener("click",function(event){
    var ctxMenu = document.getElementById("ctxMenu");
    ctxMenu.style.display = "";
    ctxMenu.style.left = "";
    ctxMenu.style.top = "";
},false);