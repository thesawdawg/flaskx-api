from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()


class Mixin():
    __abstract__ = True
    
    def save(self):
        """Save the current model instance."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Soft delete the current model instance. Can be restored using `cls.restore()`. Will be hard deleted after retain_for days."""
        self.deleted_at = db.func.now()
        db.session.commit()

    def hard_delete(self):
        """Delete the current model instance. There is no coming back. :("""
        db.session.delete(self)
        db.session.commit()

    def get_by_id(self, id):
        """
        Retrieve a model instance by its ID.
        
        :param id: Primary key of the model
        :return: Model instance or None
        """
        return self.query.get(id)

    def get_all(self):
        """
        Retrieve all instances of the model.
        
        :return: List of model instances
        """
        return self.query.all()

    def get_all_active(self):
        """
        Retrieve all active instances of the model.
        
        :return: List of model instances
        """
        return self.query.filter_by(deleted_at=None).all()

    def get_all_deleted(self):
        """
        Retrieve all deleted instances of the model.
        
        :return: List of model instances
        """
        return self.query.filter_by(deleted_at=isnot(None)).all()

    def update(self, **kwargs):
        """
        Update an existing model instance.
        
        :param id: Primary key of the model
        :param kwargs: Keyword arguments to update
        :return: Updated model instance
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def restore(self):
        """
        Restore a deleted model instance.
        
        :return: Restored model instance
        """
        self.deleted_at = None
        db.session.commit()
        return self


class BaseModel(Mixin, db.Model):
    """
    Base model with common fields and utility methods.
    All models should inherit from this class.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime)
    retain_for = db.Column(db.Integer, default=30)

    def to_dict(self):
        """
        Convert model instance to dictionary.
        Override in child classes for custom serialization.
        
        :return: Dictionary representation of the model
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

