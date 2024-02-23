import re
from os import getcwd, path
from flask import Flask, render_template, request, jsonify
from fairseq.models.transformer import TransformerModel

from worker import to_jamo

CWD = getcwd()
RESOURCES = path.join(CWD, 'resources')
DATA_BIN = path.join(RESOURCES, 'bin')
MODEL = path.join(RESOURCES, 'model_transformer')



app = Flask(__name__)

ur2sr = TransformerModel.from_pretrained(
        MODEL,
        checkpoint_file='checkpoint200.pt',
        data_name_or_path=DATA_BIN,
        bpe='sentencepiece',
        sentencepiece_model=path.join(RESOURCES, 'spm.model'),
        source_lang='ur',
        target_lang='sr'
    )

def clean_input(t):
    # remove symbols that are not Hangul nor space
    return re.sub(r'[^\s가-힣]', '', t)


def transcribe(usr_input):
    usr_input = clean_input(usr_input)
    jamo = to_jamo(usr_input)
    if len(jamo) == 0 or jamo.isspace():
        return 'N/A'
    ipa = ur2sr.translate(jamo)
    return f'[{ipa}]'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    result = transcribe(user_input)
    return jsonify({'processed_result': result})


if __name__ == '__main__':
    app.run(debug=True)
