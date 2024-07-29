from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        elif Author.query.filter(Author.name == name).first() is not None and Author.query.filter(Author.name == name).first().id != self.id:
            raise ValueError("Author must have a unique name.")
        else:
            return name
        
    @validates('phone_number')
    def validates_phone_number(self, key, phone_number):
        print(f"Validating phone number: {phone_number}")
        phone_number_int = int(phone_number)
        if isinstance(phone_number_int, int) and len(phone_number) == 10:
            return phone_number
        else:
            raise ValueError("Author must have a 10 digit phone number.")
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("title") 
    def validates_title(self, key, title):
        if len(title) == 0:
            raise ValueError("Post must have a title.")
        elif "Secret" not in title and "Won't Believe" not in title and "Top" not in title and "Guess" not in title:
            raise ValueError("Post title must contain a clickbait term.")
        else:
            return title

    @validates("summary")
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be no greater than 250 characters.")
        else:
            return summary

    @validates("content")
    def validates_content(self, key, content):
        
        if len(content) >= 250:
            return content
        else:
            raise ValueError("Post content must be atleast 250 characters.")
        
    @validates("category")
    def validates_category(self, key, category):
        if category == "Fiction" or  category == "Non-Fiction":
            return category
        else:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
