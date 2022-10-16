# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import tempfile
from flask import Flask,jsonify,send_file
import os,random
import caption 
import PIL
import pythonbible as bible
def verseidgen():
    while True:
        bookid= str(random.randint(1, 66)).zfill(2)
        chapterid= str(random.randint(1, 150)).zfill(3)
        verseid= str(random.randint(1, 150)).zfill(3)
        if(bible.is_valid_verse_id(int(bookid + chapterid + verseid)) == True):
            return int(bookid + chapterid + verseid)
def splitsentence(sentence):
    words = sentence.split()
    A = words[:len(words)//2]
    B = words[len(words)//2:]
    Astring = " ".join(A)
    Bstring = " ".join(B)
    return [Astring,Bstring]
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/")
def index():
    return "Hello World!"
@app.route('/status')
def status():
    return jsonify({'status': 'Up and Running!'}), 200
@app.route('/misato')
def misatophoto():
    path="misato"
    files=os.listdir(path)
    d=random.choice(files)
    return send_file("misato\\"+d, mimetype='image/gif')

@app.route('/asuka')
def asukameme():
    path="asuka"
    files=os.listdir(path)
    d=random.choice(files)
    temp = tempfile.NamedTemporaryFile(suffix=".jpg",delete=False)
    temp.close()
    caption.makememe("asuka\\"+d,splitsentence(bible.get_verse_text(verseidgen()))[0],splitsentence(bible.get_verse_text(verseidgen()))[1],temp.name)
    res = send_file(temp.name, mimetype='image/gif')
    return res
    

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
    