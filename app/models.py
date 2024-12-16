from .database import BaseModel, db, Mixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    """
    User model representing application users.
    
    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        
    Methods:
        set_password(password): Set a secure password hash for the user.
        check_password(password): Check if the provided password is correct.
        to_dict(): Convert user model to dictionary representation.
    """
    
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """
        Set a secure password hash for the user.
        
        :param password: Plain text password
        """
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        """
        Check if the provided password is correct.
        
        :param password: Plain text password to check
        :return: Boolean indicating password correctness
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user model to dictionary representation.
        
        :return: Dictionary of user attributes
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# class UserSchema(SQLAlchemyAutoSchema):
#     """
#     Marshmallow schema for User model serialization.
#     """
#     class Meta:
#         model = User
#         load_instance = True
#         include_relationships = True
        
#         # Exclude sensitive fields
#         exclude = ('password_hash',)

#     # Optional: Add custom fields or validation
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
