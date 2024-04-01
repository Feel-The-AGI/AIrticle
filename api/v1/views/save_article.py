"""Save Article Module"""
from flask import Blueprint, abort, session, request, jsonify
from models.article import Article
from database import db

save_blueprint = Blueprint('save_article', __name__)

@save_blueprint.route('/save_article', methods=['POST'], strict_slashes=False)
def save_article():
    """Save article to database"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"message": "Authentication required"}), 401

        data = request.get_json()
        topic = data.get('topic')
        content = data.get('content')

        if not topic or not content:
            return jsonify({"message": "Title and content are required"}), 400

        new_article = Article(
            user_id=user_id,
            title=topic,
            content=content
        )

        db.session.add(new_article)
        db.session.commit()

        # Return the ID of the new article for frontend confirmation
        return jsonify({"message": "Article Saved", "article_id": new_article.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while saving the article", "error": str(e)}), 500
