#!flask/bin/python
import argparse
import os

from flask import Flask, request, render_template, send_file
from TTS.server.synthesizer import Synthesizer
from werkzeug.utils import secure_filename


def create_argparser():
    def convert_boolean(x):
        return x.lower() in ['true', '1', 'yes']

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_checkpoint', type=str, help='path to TTS checkpoint file')
    parser.add_argument('--model_config', type=str, help='path to TTS config.json file')
    parser.add_argument('--port', type=int, default=5002, help='port to listen on.')
    parser.add_argument('--use_cuda', type=convert_boolean, default=False, help='true to use CUDA.')
    parser.add_argument('--debug', type=convert_boolean, default=False, help='true to enable Flask debug mode.')
    return parser


config = None
synthesizer = None

embedded_model_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'model')
checkpoint_file = os.path.join(embedded_model_folder, 'checkpoint.pth.tar')
config_file = os.path.join(embedded_model_folder, 'config.json')

if os.path.isfile(checkpoint_file) and os.path.isfile(config_file):
    # Use default config with embedded model files
    config = create_argparser().parse_args([])
    config.model_checkpoint = checkpoint_file
    config.model_config = config_file
    synthesizer = Synthesizer(config)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    if request.method == 'POST':
        text = request.form.get('text')
    else:
        text = request.args.get('text')
    print(" > Model input: {}".format(text))
    data = synthesizer.tts(text)
    return send_file(data, mimetype='audio/wav')

@app.route('/api/tts_upload', methods=['POST'])
def tts_upload():
    upload_file = request.files['file']
    text = str(upload_file.read()).replace('\n', '')
    print(" > Model input: {}".format(text))
    data = synthesizer.tts(text)
    return send_file(data, mimetype='audio/wav')

if __name__ == '__main__':
    if not config or not synthesizer:
        args = create_argparser().parse_args()
        synthesizer = Synthesizer(args)

    app.run(debug=config.debug, host='0.0.0.0', port=config.port)