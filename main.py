from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Replace with your desired database URI
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(main)

# main = Flask(__name__)
# main.app_context()
# main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'


# db = SQLAlchemy(main)
# db.create_all()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Article %r>' % self.id
    


@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@main.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@main.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    
    try:
        db.session.delete(article)
        db.session.commit() 
        return redirect('/posts')
    except:
        return 'При редактировании статьи произошла ошибка'


@main.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        
        
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('post_update.html', article=article)



@main.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        
        article = Article(title=title, intro=intro, text=text)
        
        try:
            if title and intro and text:
                with main.app_context():
                    db.session.add(article)
                    db.session.commit()
                    return redirect('/posts')
            else:
                return 'Заполните все пункты!'
                    # return 'Database created successfully.'
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create-article.html')





if __name__ == "__main__":
    main.run(debug=True)
