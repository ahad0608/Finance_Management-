from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///fima.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FiMa(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    date_created = db.Column(db.DateTime,default=datetime.now)
    title=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Integer,nullable=False)

    def __repr__(self) -> str:
        return f"{self.title} - {self.price}"


@app.route("/",methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        titl= request.form['title']
        pric= request.form['price']
        fima = FiMa(title=titl,price=pric)
        db.session.add(fima)
        db.session.commit()
    allfima = FiMa.query.all()
    

    return render_template('index.html',allfima=allfima)
    #return "<p>Hello, World!</p>"

@app.route("/delete/<int:sno>")
def delete(sno):
    fimadel = FiMa.query.filter_by(sno=sno).first()
    db.session.delete(fimadel)
    db.session.commit()
    return redirect('/')

if __name__ =="__main__":
    app.run(debug=True,port=8000)


