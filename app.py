from flask import Flask, render_template, request, redirect, flash
from markupsafe import escape
import pickle
import csv



vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("finalized_model.pkl", 'rb'))
app = Flask(__name__)

app.secret_key = 'Vikas'  # Needed for flashing messages (your_secret_key_here)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        news = str(request.form['news'])
        print(news)
        predict = model.predict(vector.transform([news]))[0]
        label = predict[0]
        if label == 'REAL':
            result = "🟢 Real News"
        elif label == 'FAKE':
            result = "🔴 Fake News"
        else:
            result = "⚠️ Unknown"
        return render_template("prediction.html", prediction_text ="News headline is -> {}".format(predict))



    else:
        return render_template("prediction.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the form data to a CSV file
        with open('contact_messages.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])

        flash("Your message has been sent successfully!", "success")
        return redirect("/contact")

    return render_template("contact.html")




if __name__ == '__main__':
    app.run()