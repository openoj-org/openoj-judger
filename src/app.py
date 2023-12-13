from flask import Flask, request, jsonify
from judger.judger import judge_entrance, judge
app = Flask(__name__)

@app.route('/judger', methods=['POST'])
def judger():
    try:
        json_data = request.get_json()
        result = judge_entrance(json_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'[/judger]:error': str(e)})

if __name__ == '__main__':
    app.run()