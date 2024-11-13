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
            raise ValueError("Author needs a name")

        existing_author = db.session.query(Author).filter(Author.name == name).first()

        if existing_author and (existing_author.id != self.id):
            raise ValueError(f"The name '{name}' is already taken. Please choose another name.")

        return name
    
    @validates('phone_number')
    def validates_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits and contain only numbers.")
        return phone_number

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
    @validates('title')
    def validate_title(self, key, title):
        clickbait_terms = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title.strip():
            raise ValueError("Post must have a title.")
        if not any(term in title for term in clickbait_terms):
            raise ValueError("Title must contain clickbait terms.")
        return title

    @validates('content')
    def validates_content(self, key, content):
        if isinstance(content, str) and len(content) >= 250:
            return content
        else:
            raise ValueError("Content must be a string with at least 250 characters.")
    @validates("summary")
    def validates_summary(self, key, summary):
        if isinstance(summary, str) and len(summary) <=250:
            return summary
        else:
            raise ValueError("Summary must be a maximum of 250 characters.")
    @validates("category")
    def validates_category(self, key, category):
        if category == "Fiction" or category == "Non-Fiction":
            return category
        else:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
    

               
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
