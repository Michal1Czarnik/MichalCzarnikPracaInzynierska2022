import flask
import flask_wtf
import wtforms
import wtforms.validators
import joblib

class LoginForm(flask_wtf.FlaskForm):
    url = wtforms.StringField('Sprawdzane URL: ', validators = [wtforms.validators.InputRequired()])

def token(f):
    slash = str(f.encode('utf-8')).split('/')
    total = []
    for i in slash:
        tokens = str(i).split('-')
        dot = []
        for j in range(0, len(tokens)):
            temp = str(tokens[j]).split('.')
            dot += temp
        total += tokens + dot
    total = list(set(total))
    return total

gui = flask.Flask(__name__)
gui.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
@gui.route('/', methods = ['POST', 'GET'])

def ml_prediction():
    value = LoginForm()
    if value.validate_on_submit():
        stacking_model = joblib.load('jupyter_notebook/final_model.pkl')
        tfidf = joblib.load('jupyter_notebook/vectorizer.pkl')
        temp = tfidf.transform([value.url.data])
        prediction = stacking_model.predict(temp)
        if prediction == 1:
            return flask.render_template("prediction.html", url = value.url.data, status = "to najprawdopodobniej jest phishing.")
        elif prediction == 0:
            return flask.render_template("prediction.html", url = value.url.data, status = "to najprawdopodobniej NIE jest phishing.")
    return flask.render_template("index.html", form = value)

if __name__ == '__main__':
    gui.run(debug = True)