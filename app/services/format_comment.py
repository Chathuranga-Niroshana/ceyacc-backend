from app.schemas.post import CommentResponse
from app.models.comment import Comments


def format_comment(comment: Comments) -> CommentResponse:
    commented_user = {
        "id": comment.user_id,
        "name": comment.user.name,
        "image": comment.user.image,
    }

    return CommentResponse(
        id=comment.id,
        comment=comment.comment,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=commented_user,
        parent_comment_id=comment.parent_comment_id,
        replies=(
            [format_comment(reply) for reply in comment.replies]
            if comment.replies
            else []
        ),
    )
