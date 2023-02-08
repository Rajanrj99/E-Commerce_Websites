from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_URI ,SECRET_KEY
from flask_login import LoginManager



app=Flask(__name__)

@app.template_filter()
def to_str(value):
    return str(value)
    

db=SQLAlchemy()






def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_ECHO']=True
    app.secret_key=SECRET_KEY
    
    db.init_app(app)
    print("DB initialized successfully")

    
    from .route import  views
    app.register_blueprint(views)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     db.session.commit()
        
    from .models.user import User
    
    login_manger=LoginManager()
    login_manger.login_view='views.login_page'
    login_manger.init_app(app)
    login_manger.login_message_category='info'

    
    
    @login_manger.user_loader
    def load_user(user_id):
        id=User.query.get(user_id)
        if id:
            return id
        else:
            return None
        
    
    

    return app
        
