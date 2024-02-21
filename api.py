from flask import Flask, request, jsonify
app = Flask(__name__)


class Question:
    def __init__(self, text, options):
        self.text = text 
        self.options = options 

class Option:
    def __init__(self, text, indicators):
        self.text = text
        self.indicators = indicators #Map (indicatorName:value, ...)         

class Response:
    def __init__(self, question_text, selected_option):
        self.question_text = question_text
        self.selected_option = selected_option

class Indicator:
    def __init__(self, preferences, value = 0):
        self.preferences = preferences
        self.value = value

class Assessment:
    def __init__(self):
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def build_outcome_code(self):
        for question in self.questions:
            print(question)

        

    
class Outcome:
    def __init__(self, code, title, subtitle=None):
        self.code = code
        self.title = title
        self.subtitle = subtitle







@app.route('/score', methods=['POST'])
def score_assessment():
    # Assume the request contains a list of responses
    data = request.json
    # Here you would convert that JSON into Assessment and Response objects
    # For simplicity, let's assume a simple data structure and a predefined assessment
    responses = [Response(d['question_text'], d['selected_option']) for d in data['responses']]
   
    
    return


if __name__ == '__main__':
    app.run(debug=True)
