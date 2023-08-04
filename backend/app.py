from flask import Flask, request, jsonify
from flask_cors import CORS

from process import process_files, query_collection, consulta, process_info

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'ok'

@app.route('/insert_bloque/<texto>/<database>/<titulo>/<filename>')
def insertInfo(texto,database,titulo,filename):
    result =process_info(texto,database,titulo,filename)
    print("Ha terminado la ejecucion...................")
    return result


@app.route('/consulta/<pregunta>',methods=['GET'])
def consultame(pregunta):
    result = consulta(pregunta)
    return jsonify(result)


@app.route('/process', methods=['POST'])
def process():
    documents = request.files.getlist('documents')
    process_files(documents)
    response = {'success': True}
    return jsonify(response)


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('text')
    results = query_collection(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
