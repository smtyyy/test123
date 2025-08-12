from flask.views import MethodView
from flask_smorest import Blueprint
from models import db, Score, ScoreSchema, ChatMessage, ChatMessageSchema


blp = Blueprint("typing", __name__, url_prefix="/api", description="Typing API")


@blp.route("/scores")
class ScoresResource(MethodView):
    @blp.response(200, ScoreSchema(many=True))
    def get(self):
        return Score.query.order_by(Score.timestamp.desc()).all()

    @blp.arguments(ScoreSchema)
    @blp.response(201, ScoreSchema)
    def post(self, data):
        score = Score(**data)
        db.session.add(score)
        db.session.commit()
        return score


@blp.route("/chat")
class ChatResource(MethodView):
    @blp.response(200, ChatMessageSchema(many=True))
    def get(self):
        messages = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).limit(50).all()
        return list(reversed(messages))

    @blp.arguments(ChatMessageSchema)
    @blp.response(201, ChatMessageSchema)
    def post(self, data):
        message = ChatMessage(**data)
        db.session.add(message)
        db.session.commit()
        return message
