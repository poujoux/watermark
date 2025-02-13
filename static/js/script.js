let uplflg = false; //Prevents another upload from occuring during an ongoing process
let prvwflg = false; //Prevents another preview from occuring during an ongoing preview

let fileonurl = null; //Preserves the URL of a created file

let numberi;
let numberp;



function execaddfile(addfile) {
    document.getElementById(addfile).click();
}


document.addEventListener("DOMContentLoaded", function () {
    const listbox = document.getElementById("datalistbox");
    const positions = ["lefttop", "righttop", "leftbottom", "rightbottom"];
    positions.forEach(el => {
        const option = document.createElement("option");
        option.value = el.trim();
        listbox.appendChild(option);
    });

    document.getElementById("datalistvalue")?.addEventListener("input", async function () {
            
        const inputi = document.getElementById("addfilei");
        const inputw = document.getElementById("addfilew");
        const listboxInput = document.getElementById("datalistvalue");

        const imgl = document.getElementById("imgl");
        const inft = document.getElementById("inft");

        const listboxvalue = listboxInput.value.trim();

        if (prvwflg) {
            imgl.src = "";
            prvwflg = false;

            inft.style.display = "block";
             
        }

        const valuepart = listboxvalue.includes(" ") && listboxvalue.includes("%") && listboxvalue.split(" ").length === 2 ? listboxvalue.split(" ") : null;

        numberi = valuepart && positions.includes(valuepart[0]) ? [valuepart[0], valuepart[1].replace(/\D/g, "")] : null;
        numberi = numberi[1] == 1 ? [numberi[0], 2] : numberi;

        numberp = numberi && (100>=Number(numberi[1]) && Number(numberi[1]) > 0) ? Number(numberi[1]) : null;

        if (!numberp){
            return;
        }

        if (numberp) {
            imgl.src = "";

            const formData = new FormData();
            formData.append("listbox", numberi);
            formData.append("Status", "a");

            try {
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok){
                    const errormsg = await response.json();
                    throw new Error(errormsg.message);
                }

                const data = await response.json();

                if (data.Status === "SUCCESS") {
                    let newSrc = data.Data + "?timestamp=" + Date.now();
                    imgl.src = newSrc;
                }
            } catch (error) {
                alert("An error occurred while uploading: " + (error.message || "Unknown error"));

            } finally {
                prvwflg = true;
                inft.style.display = "none";
                

            }
        }
    });
});


document.getElementById("addfilef").addEventListener("submit", async (event) => {
    if(numberp && !uplflg){
        await sendfiles(event);
    }
    else{
        event.preventDefault(); 
        if(uplflg){
            alert("Please wait while it is processing");
        }
        else{
            alert("Please enter a valid statement");
        }

        return;
    }
});


async function sendfiles(event) {
    event.preventDefault();

    uplflg = true;

    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        if (data["Status"] === "SUCCESS") {
            await uploadFiles();
        } else {
            alert(data.Status);
        }
    } catch (error) {
        alert("An error occurred while uploading ", (error.message || "Unknown error"));
        uplflg = false; 
    }
}


async function uploadFiles() {
    try {
        const response = await fetch("/takelist");
        const result = await response.json();

        if(!response.ok){
            throw new Error(result.message);
        }

        const files = result["files"];

        await watermark(files);

    } catch (error) {
        alert("An error occurred while uploading: " + (error.message || "Unknown error"));
        uplflg = false;
    }
}


async function watermark(files) {
    await logc(numberi);

    let nrfiles;
    if (files.length > 1) {
        nrfiles = files.slice(0, -1).map(file => watermarkp(file));
    } else {
        nrfiles = [watermarkp(files[0])];
    }

    try {
        await Promise.all(nrfiles);

        const rdata = await fetch(`/watermark/end?timestamp=${Date.now()}`, { method: "POST" });
        const lastfile = await rdata.blob();

        if (fileonurl) {
            URL.revokeObjectURL(fileonurl);
        }

        fileonurl = URL.createObjectURL(lastfile);
        info = document.createElement("a");
        info.href = "#";
        info.textContent = "It is being downloaded";

        window.open(fileonurl, "_blank");

        document.body.appendChild(info);
        setTimeout(() => {
            document.body.removeChild(info);
            info.remove();
        }, 1000);

    } catch (error) {
        alert("An error occurred: " + (error.message || "Unknown error"));
        uplflg = false;
    } finally {
        uplflg = false;
    }
}


function watermarkp(file) {
    return fetch(`/watermark/${file.name}`, {
        method: "POST",
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error("The response is not ok");})
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            return data;
        })
        .catch(error => {
            throw(error.message || "Unknown error");
            uplflg = false;
        });
}

function logc(message) {
    fetch("/watermark/message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "message": message[0], "size": message[1]})
    })
    .then(response => {
        if(!response.ok){
            return response.json().then(data => {
                throw new Error(data.message || "Unknown error");
            })
        }})
    .catch(error => {
        alert(error.message);
        uplflg = false;
    });
}

