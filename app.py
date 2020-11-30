from flask import Flask, request, jsonify, render_template
from predict import model_fn, predict_fn

app = Flask(__name__)

model = model_fn('model')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_output():
    if request.method=='POST' and request.form['review'] is not None:
        try:
            review = request.form.get('review')
        except:
            return jsonify({'message':'Error. No data found.', 'status':0})
        
        if len(review.strip()) == 0:
            return jsonify({'message':'Error. No data found.', 'status':0})
        
        try:
            result = predict_fn(review, model)
        except Exception as e:
            print(e)
            return jsonify({'message':'Error. Some problem in prediction function.'+str(e), 'status':0})
        
        return jsonify({'message':'success', 'prediction':result, 'status':1})
    return jsonify({'message':'Error. Inappropriate request received.', 'status':0})

if __name__ == '__main__':
	app.run(debug=True)
