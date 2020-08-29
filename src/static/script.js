function dropdown(id, btnid, spin) {
    var d = document.getElementById(id);
    var btn = document.querySelector("#" + btnid + " svg");
    if (d.className.indexOf("w3-show") === -1) {
        d.className += " w3-show";
//        btn.className = btn.className.replace("fa-plus", "fa-times");
        if (spin) btn.style.transform = "rotate(135deg)"
    } else {
        d.className = d.className.replace(" w3-show", "")
        if (spin) btn.style.transform = "rotate(0deg)"
//        btn.className = btn.className.replace("fa-times", "fa-plus");
    }
}

var files = [];
window.addEventListener("load", function() {
    files = [];
})
function uploadFile() {
    // If this doesn't work, then use this method:
    // - Instead of having a files array, just add all of the file inputs
    // to a div.w3-hide and just make the form submit with action attribute
    // No need of fetch, or formdata
    // NOTE: You may need to add content-type = multipart/form-data as attribute to form element
    document.getElementById("addFile").disabled = true
    var fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.multiple = "multiple";
    fileInput.click();
    fileInput.addEventListener("change", function () {
        for (var i = 0; i < fileInput.files.length; i++) {
            files.push(fileInput.files[i]);
            var li = document.createElement("li");
            li.className = "w3-bar";
            var btn = document.createElement("button");
            btn.innerHTML = '<i class="fas fa-trash"></i>';
            btn.className = "w3-bar-item w3-right w3-margin-right w3-button w3-red w3-hover-pale-red";
            btn.addEventListener("click", function (e) {delFile(e, fileInput.files[i])});
            var span = document.createElement("span");
            span.className = "w3-bar-item";
            span.innerText = fileInput.files[i].name;
            li.appendChild(span);
            li.appendChild(btn);
            document.querySelector("#uploadFile #fileList").appendChild(li);
        }
    });
    document.getElementById("addFile").disabled = false;
}

function delFile(e, f) {
    // If this doesn't work, then use this method:
    // - Instead of having a files array, just add all of the file inputs
    // to a div.w3-hide and just make the form submit with action attribute
    // No need of fetch, or formdata
    // NOTE: You may need to add content-type = multipart/form-data as attribute to form element
    files = files.filter(i => i !== f);
    document.getElementById("fileList").innerHTML = "";
    for (var i = 0; i < files.length; i++) {
        var li = document.createElement("li");
        li.className = "w3-bar";
        var btn = document.createElement("button");
        btn.innerHTML = '<i class="fas fa-trash"></i>';
        btn.className = "w3-bar-item w3-right w3-margin-right w3-button w3-red w3-hover-pale-red";
        btn.addEventListener("click", function (e) {delFile(e, files[i])});
        var span = document.createElement("span");
        span.className = "w3-bar-item";
        span.innerText = files[i].name;
        li.appendChild(span);
        li.appendChild(btn);
        document.querySelector("#uploadFile #fileList").appendChild(li);
    }
}

document.querySelector("#uploadFile form.w3-container").addEventListener("submit", function (e) {
    // If this doesn't work, then use this method:
    // - Instead of having a files array, just add all of the file inputs
    // to a div.w3-hide and just make the form submit with action attribute
    // No need of fetch, or formdata
    // NOTE: You may need to add content-type = multipart/form-data as attribute to form element
    e.preventDefault();
    if (!files.length) return;
    var fd = new FormData();
    fd.append("type", "upload_file");
    fd.append("path", document.querySelector("#uploadFile form.w3-container button[type='submit']").value);
    for (var i = 0; i < files.length; i++) {
        fd.append("file" + i, files[i]);
    }
    document.querySelector("#uploadFile form.w3-container #spinner").display = "initial";
    fetch("/new", {
        method: "POST",
        body: fd
    }).then(r => r.json()).then(d => {if (d === "All good") window.location.reload()})
})