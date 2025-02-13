import os
import time
import shutil
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template, send_file, abort

app = Flask(__name__, static_folder="static", template_folder="templates")

app.config["UPLOAD_PATH"] = os.path.join("static", "images")
app.config["UPLOAD_PATHtemp"] = os.path.join("static", "images", "img1")


def logger(name, e="enter"):
    if e=="o":
        print(9*"-", "EXITING FROM: ", name, 9*"-", end="\n")

    else: 
        print(9*"-", "ENTERING TO: ", name, 9*"-", end="\n")


def isitvalid(file):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/", methods=["POST", "GET"])
def m():       
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not request.headers.get("Referer"):
        abort(403)

    logger("UPLOAD")

    if(request.form.get("Status") == "a"):
        logger("UPLOAD A")

        dirpath = app.config["UPLOAD_PATHtemp"]

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            os.chmod(dirpath, 0o777)

        sfile = os.path.join(app.config["UPLOAD_PATH"], "file.png")
        watermimgpath = os.path.join(app.config["UPLOAD_PATH"], "watermrk.png")

        if not os.path.exists(sfile):
            imgbckg = Image.new("RGBA", (80,80), "black")
            imgwtrm = Image.new("RGBA", (20,20), "gray")

            imgbckg.save(sfile)
            imgwtrm.save(watermimgpath)

        print(request.form, end="\n")
        pos = request.form["listbox"].split(",")
        print(pos)
        size = 0.01*int(pos[1])

        try:
            watermimg = Image.open(watermimgpath)
            file = Image.open(sfile)
        except IOError as e:
            return jsonify({"Error": str(e)}), 404


        watermimgs = (int(file.width*size), int(file.height*size))

        try:
            watermimg = watermimg.resize(watermimgs, Image.Resampling.LANCZOS)
        except Exception as e:
            print("An error occured while resizing: ", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500
        

        loccord = [(0,0), (file.width - watermimgs[0], 0), (0,file.height-watermimgs[1]), (file.width - watermimgs[0], file.height - watermimgs[1])]

        pospoint = ["lefttop", "righttop", "leftbottom", "rightbottom"]
        locpos = dict(zip(pospoint, loccord))

        file.paste(watermimg, locpos.get(pos[0]), watermimg.split()[3])

        filepath = os.path.join(app.config["UPLOAD_PATH"], "testimg.png") 

        file.save(filepath)

        print({"Status": "SUCCESS", "Data": filepath})
        return jsonify({"Status": "SUCCESS", "Data": filepath}), 200

            
    try:
        print("-------OUTPUT OF THE FILES------\n", request.files)
        print("-------OUTPUT OF WATERMARK------\n", request.files.getlist("watermrkpng")[0])

        files = request.files.getlist("files")
        watermark = request.files.getlist("watermrkpng")[0]
        files.append(watermark)

        print("-------OUTPUT OF THE FILES------\n", files)

        dirpath = app.config["UPLOAD_PATHtemp"]

        for file in files:
            if file and file.filename and isitvalid(file):
                print("File is valid")
                print(9*"-", end="\n")
                print(file, end="\n")

                if file == watermark:

                    wfilepath = os.path.join(app.config["UPLOAD_PATH"], "watermark.png")
                    print("watermark: ", wfilepath, end="\n")

                    file.save(wfilepath)
                    return jsonify({"Status": "SUCCESS"}), 200


                filepath = os.path.join(app.config["UPLOAD_PATHtemp"], secure_filename(file.filename))
                file.save(filepath)

            else:
                filenum = len(files)
                print(watermark)
                if not watermark and filenum<3:
                    return jsonify({"Status": "Please fill in all the inputs"}), 400
                elif filenum<3:
                    return jsonify({"Status": "Please fill in the files input"}), 400
                elif not watermark:
                    return jsonify({"Status": "Please fill in the watermark input"}), 400

                print("File is not valid")
                return jsonify({"Status": "FAIL"}), 400
            

        return jsonify({"Status": "SUCCESS"}), 200
        
    except Exception as e:
        print("Error: " + e)
        return jsonify({"Status": str(e)})
        
    logger("UPLOAD", "o")
    
@app.route("/takelist", methods=["GET"])
def takelist():
    if not request.headers.get("Referer"):
        abort(403)

    logger("TAKELIST")

    files = [{"name": filename} for filename in os.listdir(app.config["UPLOAD_PATHtemp"])]

    if(not bool(files)):
            raise Exception("No files")

    files.append({"name": "end"})

    print(files)

    logger("TAKELIST", "o")

    return jsonify({"Status": True, "files": files}), 200

    
locationi = ""
sizei = ""

@app.route("/watermark/<filename>", methods=["POST", "GET"])
def watermark(filename):
    global locationi
    global sizei 

    logger("WATERMARK")

    if filename == "message":
        locationi = request.get_json().get("message", "")
        sizei = int(request.get_json().get("size", ""))*0.01

        print("sizei: ", sizei)

        return jsonify({"Status": "Success"}), 200


    filepath = os.path.join(app.config["UPLOAD_PATHtemp"], filename)


    if filename == "end":
        archdir = os.path.join(app.config["UPLOAD_PATH"], "archive")
        
        curdir = os.path.join(os.path.abspath(__file__))
        imgdir = os.path.join(curdir, "static", "images", "img1")
        imgdir1 = os.path.join(curdir, app.config["UPLOAD_PATHtemp"])


        try:

            if os.path.exists(app.config["UPLOAD_PATH"]):
                shutil.make_archive(archdir, "zip", app.config["UPLOAD_PATHtemp"])
                print("The archive has been created")

            #if the script cannot access the static/images directory this one will probably fail too

            elif os.path.exists(imgdir1):
                print("Failed while creating the archive. Trying again...")

                curdir = os.path.join(os.path.abspath(__file__))
                archdir1 = os.path.join(curdir, app.config["UPLOAD_PATH"], "archive")
                shutil.make_archive(archdir1, "zip", imgdir1)
                
                print("The archive has been created")



        except Exception as e:
            print("Error while creating the archive: ", e)
                
            return jsonify({"Error": "Error while creating the archive: " + str(e)}), 500

        response = send_file(f"{archdir}.zip", as_attachment=True)

        shutil.rmtree(app.config["UPLOAD_PATHtemp"])

        return response

    try:
        file = Image.open(filepath)
        watermimgpath = os.path.join(app.config["UPLOAD_PATH"], "watermark.png")

        print(watermimgpath, end="\n")
        print("\n1", filepath, end="\n")

        watermimg = Image.open(watermimgpath)

    except IOError as e:
        return jsonify({"Error": str(e)}), 404


    if file.mode == "RGBA":
        file = file.convert("RGB")

    if watermimg.mode != "RGBA":
        watermimg = watermimg.convert("RGBA")

    if not os.path.exists(app.config["UPLOAD_PATHtemp"]):
        os.makedirs(imgdir, exist_ok=True)
        os.chmod(imgdir, 0o755)

    watermimgs = (int(file.width*sizei), int(file.height*sizei))

    try:
        watermimg = watermimg.resize(watermimgs, Image.Resampling.LANCZOS)
    except Exception as e:
        print("An error occured while resizing: ", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

    loccord = [(0,0), (file.width - watermimgs[0], 0), (0,file.height-watermimgs[1]), (file.width - watermimgs[0], file.height - watermimgs[1])]
    pospoint = ["lefttop", "righttop", "leftbottom", "rightbottom"]

    locpos = dict(zip(pospoint, loccord))


    file.paste(watermimg, locpos.get(locationi), watermimg.split()[3])
    file.save(os.path.join(app.config["UPLOAD_PATHtemp"], filename))

    logger("WATERMARK", "o")

    return jsonify({"Status": True}), 200




if __name__ == "__main__":
    app.run(debug=True)


'''

@app.route("/log", methods=["POST"])
def log():
    message = request.get_json()
    print(f"Log message received: {message.get('message', 'No message')}")
    return jsonify({"sts": message.get("message")}), 200

'''
