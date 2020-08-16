import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import flask
from nltk.tokenize import sent_tokenize, word_tokenize 


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()


app = flask.Flask(__name__, template_folder = 'templates')
@app.route('/', methods=['GET', 'POST'])
IMAGE_FILE = str(flask.request.form['Url'])


with io.open(IMAGE_FILE, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.document_text_detection(image=image)

docText = response.full_text_annotation.text
print(docText)

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        oneM = flask.request.form['oneM']
        oneMlist = oneM.split(",")
        twoM = flask.request.form['twoM']
        twoMlist = twoM.split(",")
        data = [] 
  
# iterate through each sentence in the file 
        for i in sent_tokenize(docText): 
            temp = [] 
      
    # tokenize the sentence into words 
            for j in word_tokenize(i): 
                temp.append(j.lower()) 
  
            data.append(temp)
        count = 0
        for n in data:
            for m in oneMlist:
                if n == m:
                    count += 1
            for p in twoMlist:
                if n == p:
                    count += 2
            return count
        
        input_variables = pd.DataFrame([[oneM, twoM]], columns = ['oneM', 'twoM'], dtype=string)
        
        
        return flask.render_template('main.html', original_input = {'Words that are important in the answer (1 mark)':oneM, 'Words that are important in the answer (2 mark)':twoM}, result = count,)

if __name__ == '__main__':
    app.run()

#pages = response.full_text_annotation.pages
#for page in pages:
#    for block in page.blocks:
#        print('block confidence:', block.confidence)
#
#        for paragraph in block.paragraphs:
#            print('paragraph confidence:', paragraph.confidence)#
#
#            for word in paragraph.words:
#                word_text = ''.join([symbol.text for symbol in word.symbols])##
#
#                print('Word text: {0} (confidence: {1}'.format(word_text, word.confidence))#
#
#                for symbol in word.symbols:
#                    print('\tSymbol: {0} (confidence: {1}'.format(symbol.text, symbol.confidence))
