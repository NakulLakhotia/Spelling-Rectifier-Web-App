from flask import Flask, render_template, request, redirect,abort
from textblob import TextBlob
from spellchecker import SpellChecker
import re
import os

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.txt']

@app.route("/", methods=["GET", "POST"])
def index():
    correct = ""
    a=""
    list1=[]
    list2=[]
    misspelled=[]
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        #print("Type :",type(request.files))
        #print("Files :",request.files)
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file.filename != '':
            file_ext = os.path.splitext(file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                print("Please upload a file type of .txt only")
                return abort(404)
        if file:
            f = open(file.filename,"r+")
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