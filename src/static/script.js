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
var xhr = new XMLHttpRequest();
//window.addEventListener("load", function() {
//    files = [];
//})

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
            var file = fileInput.files[i]
            btn.addEventListener("click", function () {delFile(file)});
            btn.type = "button"
            var span = document.createElement("span");
            span.className = "w3-bar-item";
            span.innerText = fileInput.files[i].name;
            var small = document.createElement("span");
            small.className = "w3-bar-item w3-small w3-text-gray";
            var fileSize = fileInput.files[i].size;
            if (fileSize > 1024 * 1024) small.innerText = (Math.round(fileSize * 100 / (1024 * 1024)) / 100).toString() + " MiB";
            else small.innerText = (Math.round(fileSize * 100 / (1024)) / 100).toString() + " KiB";
            li.appendChild(span);
            li.appendChild(small);
            li.appendChild(btn);
            document.querySelector("#uploadFile #fileList").appendChild(li);
        }
    });
    document.getElementById("addFile").disabled = false;
}

function delFile(f) {
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
        btn.type = "button"
        btn.className = "w3-bar-item w3-right w3-margin-right w3-button w3-red w3-hover-pale-red";
        btn.addEventListener("click", function () {delFile(files[i])});
        var span = document.createElement("span");
        span.className = "w3-bar-item";
        span.innerText = files[i].name;
        var small = document.createElement("span");
        small.className = "w3-bar-item w3-small w3-text-gray";
        var fileSize = files[i].size;
        if (fileSize > 1024 * 1024) small.innerText = (Math.round(fileSize * 100 / (1024 * 1024)) / 100).toString() + " MiB";
        else small.innerText = (Math.round(fileSize * 100 / (1024)) / 100).toString() + " KiB";
        li.appendChild(span);
        li.appendChild(small);
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
    document.querySelector("#uploadFile #addFile").disabled = true;
    document.querySelector("#uploadFile #uploadFileBtn").disabled = true;
    document.querySelector("#uploadFile #progress").className = document.querySelector("#uploadFile #progress").className.replace("w3-hide", "");
    xhr.upload.addEventListener("progress", updateFileUploadProgress, false);
    xhr.addEventListener("load", fileUploaded, false);
    xhr.addEventListener("error", fileUploadFailed, false);
    xhr.addEventListener("abort", fileUploadCancelled, false);
//    fetch("/new", {
//        method: "POST",
//        body: fd
//    }).then(r => r.json()).then(d => {if (d === "All good") window.location.reload()})
    xhr.open("POST", "/new");
    xhr.send(fd);
})

function cancelFileUpload() {
    xhr.abort();
    document.getElementById('uploadFile').classList.toggle('w3-show');
}

function updateFileUploadProgress(e) {
    if (e.lengthComputable) {
        var percent = Math.round(e.loaded * 100 / e.total);
        document.querySelector("#uploadFile #progress #progress-bar").style.width = percent + "%";
        document.querySelector("#uploadFile #progress #progress-bar").innerText = percent.toString() + "%";
    }
}

function fileUploaded(e) {
    window.location.reload();
}

function fileUploadFailed(e) {
    alert("Upload failed due to an error.");
}

function fileUploadCancelled(e) {
    alert("File upload cancelled.");
}

function rename(type, id, old_name) {
    var qs = "#renameModal[data-type='" + type + "']";
    document.querySelector(qs).classList.toggle("w3-show");
    document.querySelector(qs + " #new").value = old_name
    document.querySelector(qs + " #new").focus();
    document.querySelector(qs + " #id").value = id
}

function del(type, id, fn) {
    var qs = "#deleteModal[data-type='" + type + "']";
    document.querySelector(qs).classList.toggle("w3-show");
    document.querySelector(qs + " #id").value = id
    document.querySelector(qs + " #file_name").innerText = fn
}