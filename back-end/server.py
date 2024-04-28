from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime
from model import detect_sentiment, BAD, GOOD, NOMAL


app = Flask(__name__)
CORS(app)

@app.route("/analyst-file", methods=['POST'])
def get_analyst():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_contents = file.read()
    array_comments = file_contents.decode('utf-8').split('---')
    print(array_comments)
    
    start_time =  datetime.now()
    number_good_comments = 0
    number_bad_comments = 0
    number_nomal_comments = 0

    try:
        for comment in array_comments:
            sentiment = detect_sentiment(comment)
            if sentiment == GOOD:
                number_good_comments += 1
            if sentiment == BAD:
                number_bad_comments += 1
            if sentiment == NOMAL:
                number_nomal_comments += 1
            
        end_time = datetime.now()
        duration_time = end_time - start_time
        return jsonify({
            'number_good_comments': number_good_comments, 
            'number_bad_comments': number_bad_comments, 
            'number_nomal_comments': number_nomal_comments, 
            'duration_time': str(duration_time)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/rate-comment", methods=['POST'])
def rate_comment():
    comment = request.args.get('comment')
    if comment == None:
        return 'No target comment!', 400

    try:
        sentiment = detect_sentiment(comment)
        if sentiment == GOOD:
            return 'GOOD'
        if sentiment == BAD:
            return 'BAD'
        if sentiment == NOMAL:
            return 'NOMAL'
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/rate-list-comments", methods=['POST'])
def rate_list_comments():
    data = request.json
    comments = data.get("comments")
    if len(comments) == 0:
        return 'No target comment!', 400

    start_time =  datetime.now()
    number_good_comments = 0
    number_bad_comments = 0
    number_nomal_comments = 0

    try:
        for comment in comments:
            sentiment = detect_sentiment(comment)
            if sentiment == GOOD:
                number_good_comments += 1
            if sentiment == BAD:
                number_bad_comments += 1
            if sentiment == NOMAL:
                number_nomal_comments += 1
            
        end_time = datetime.now()
        duration_time = end_time - start_time
        return jsonify({
            'number_good_comments': number_good_comments, 
            'number_bad_comments': number_bad_comments, 
            'number_nomal_comments': number_nomal_comments, 
            'duration_time': str(duration_time)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
