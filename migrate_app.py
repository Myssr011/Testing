#!/usr/bin/env python3
"""
Flask application for database migration
Simple Flask app to run database migrations
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:mariabelajar@if.unismuh.ac.id:3388/iqball')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'max_overflow': 20
}

# Initialize extensions
db = SQLAlchemy(app)

# Import and register models with Flask-SQLAlchemy
from database.models import Base

# Create new model classes that inherit from db.Model instead of Base
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', 'reviewer', name='userrole'), default='user', index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Abstract(db.Model):
    __tablename__ = 'abstracts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(200), nullable=False, index=True)
    institution = db.Column(db.String(200), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    abstract_text = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.Enum('pdf', 'docx', 'txt', name='filetype'), nullable=False)
    language = db.Column(db.String(10), default='id', index=True)
    upload_date = db.Column(db.Date, nullable=False, index=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    processed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class SimilarityResult(db.Model):
    __tablename__ = 'similarity_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_abstract_id = db.Column(db.Integer, db.ForeignKey('abstracts.id', ondelete='CASCADE'), nullable=False, index=True)
    target_abstract_id = db.Column(db.Integer, db.ForeignKey('abstracts.id', ondelete='CASCADE'), nullable=False, index=True)
    similarity_score = db.Column(db.DECIMAL(5, 4), nullable=False, index=True)
    similarity_label = db.Column(db.Enum('very_low', 'low', 'medium', 'high', 'very_high', name='similaritylabel'), nullable=False, index=True)
    algorithm_used = db.Column(db.String(50), default='cosine_similarity')
    threshold_used = db.Column(db.DECIMAL(3, 2), default=0.70)
    detailed_results = db.Column(db.JSON)
    processing_time = db.Column(db.DECIMAL(8, 3))
    checked_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    checked_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class DetectionBatch(db.Model):
    __tablename__ = 'detection_batches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batch_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    total_abstracts = db.Column(db.Integer, nullable=False)
    total_comparisons = db.Column(db.Integer, nullable=False)
    completed_comparisons = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed', 'cancelled', name='batchstatus'), default='pending', index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    processing_time = db.Column(db.DECIMAL(10, 3))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class BatchAbstract(db.Model):
    __tablename__ = 'batch_abstracts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('detection_batches.id', ondelete='CASCADE'), nullable=False, index=True)
    abstract_id = db.Column(db.Integer, db.ForeignKey('abstracts.id', ondelete='CASCADE'), nullable=False, index=True)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_level = db.Column(db.Enum('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', name='loglevel'), nullable=False, index=True)
    module = db.Column(db.String(100), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)

# Initialize migrations
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Plagiarism Detection System - Database Migration App"

if __name__ == '__main__':
    app.run(debug=True)
