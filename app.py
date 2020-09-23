from flask import Flask, render_template, request, redirect,abort,flash
from textblob import TextBlob
from spellchecker import SpellChecker
import re
import getpass
import os



username = getpass.getuser()
UPLOAD_FOLDER = 'C:/Users/'+username+'/Desktop'

print(UPLOAD_FOLDER)
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    correct = ""
    a=""
    list1=[]
    list2=[]
    misspelled=[]
    error=""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file.filename != '':
            file_ext = os.path.splitext(file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                print("Please upload a .txt file type only")
                return abort(400)

        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print('C:/Users/'+username+'/Desktop/'+file.filename)
            f = open('C:/Users/'+username+'/Desktop/'+file.filename,"r+")
            filecontent=f.read()
            a= str(filecontent)
            b = TextBlob(a)
            correct= str(b.correct())

            # remove all punctuations before finding possible misspelled words
            s = re.sub(r'[^\w\s]', '', filecontent)
            #print("Text without punctuations:\n", s)
            wordlist = s.split()
            spell = SpellChecker()
            # find those words that may be misspelled
            misspelled = list(spell.unknown(wordlist))
            for word in misspelled:
                # Get the one `most likely` answer
                list1.append(spell.correction(word))
                # Get a list of `likely` options
                list2.append(spell.candidates(word))

    return render_template('index.html',a=a ,correct=correct,misspelled=misspelled,list1=list1,list2=list2,len=len(misspelled) ,len1=len(list1))


if __name__ == "__main__":
    app.run(debug=True, threaded=True)