from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

def calculate_health_score(age,sleep,exercise,junk,pollution):
    score = 100

    if age >50:
        score -= 10
    else:
        score -=5

    if sleep < 6:
        score -= 20
    elif sleep < 7:
        score -= 10
    if exercise == "low":
        score -= 20
    elif exercise == "medium":
        score -= 10
    
    if junk =="high":
        score -= 20
    elif junk =="medium":
        score -= 10

    if pollution == "high":
        score -= 15
    elif pollution == "medium":
        score -= 8
    return max(score, 0)
def get_risk(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 50:
        return "Moderate Risk"
    else:
        return "High Risk"
def get_suggestions(sleep, exercise, junk, pollution):
    tips = []

    if sleep < 7:
        tips.append("Improve sleep to at least 7-8 hours.")

    if exercise == "low":
        tips.append("Start with 30 minutes of walking daily.")

    if junk == "high":
        tips.append("Reduce junk food intake and eat healthier meals.")

    if pollution == "high":
        tips.append("Avoid outdoor activities during high pollution days and consider using air purifiers.")

    if not tips:
        tips.append("Great job! Maintain your healthy lifestyle.")

    return tips
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        age = int(request.form['age'])
        sleep = float(request.form['sleep'])
        exercise = request.form['exercise']
        junk = request.form['junk']
        pollution = request.form.get('pollution', 'low')
        health_score = calculate_health_score(age, sleep, exercise, junk, pollution)
        risk_level = get_risk(health_score)
        suggestions = get_suggestions(sleep, exercise, junk, pollution)
        print(suggestions)
        return render_template('index.html', score=health_score, risk=risk_level, suggestions=suggestions)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message', '').lower()

    if "sleep" in user_message:
        reply = "Try to maintain 7-8 hours of sleep daily."
    elif "diet" in user_message:
        reply = "Eat more fruits, vegetables, and avoid processes food."
    elif "exercise" in user_message:
        reply = "Aim for at least 150 minutes of moderate exercise per week."
    elif "pollution" in user_message:
        reply = "Limit outdoor activities on high pollution days and consider using air purifiers." 
    else:
        reply = "Sorry, I can only provide tips on sleep, diet, exercise, and pollution. Please ask about one of these topics." 
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)