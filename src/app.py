from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        json_data = request.get_json()

        #TODO
        print(json_data)
        print(type(json_data['key1']))
        result = {'success': True}

        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()