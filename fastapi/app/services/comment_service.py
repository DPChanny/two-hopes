from sqlalchemy.orm import Session
from entities.comment import Comment
from entities.post import Post
from dtos.comment_dto import (
    CommentDTO,
    AddCommentRequestDTO,
    GetCommentListRequestDTO,
    GetCommentListResponseDTO,
    UpdateCommentRequestDTO,
)
from dtos.base_dto import BaseResponseDTO
from exception import CustomException, handle_exception


def add_comment_service(
    dto: AddCommentRequestDTO, db: Session
) -> BaseResponseDTO[CommentDTO]:
    try:
        post = db.query(Post).filter(Post.post_id == dto.post_id).first()
        if not post:
            raise CustomException(404, "Post not found.")

        comment = Comment(
            post_id=dto.post_id, content=dto.content, author=dto.author
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return BaseResponseDTO(
            success=True,
            code=201,
            message="Comment added successfully.",
            data=CommentDTO.model_validate(comment),
        )
    except Exception as e:
        handle_exception(e, db)


def get_comment_list_service(
    dto: GetCommentListRequestDTO, db: Session
) -> GetCommentListResponseDTO:
    try:
        query = db.query(Comment)

        if dto.post_id:
            query = query.filter(Comment.post_id == dto.post_id)

        comments = query.all()
        comment_dtos = [CommentDTO.model_validate(c) for c in comments]

        return GetCommentListResponseDTO(
            success=True,
            code=200,
            message="Comment list retrieved successfully.",
            data=comment_dtos,
        )
    except Exception as e:
        handle_exception(e, db)


def update_comment_service(
    comment_id: int, dto: UpdateCommentRequestDTO, db: Session
) -> BaseResponseDTO[CommentDTO]:
    try:
        comment = (
            db.query(Comment).filter(Comment.comment_id == comment_id).first()
        )
        if not comment:
            raise CustomException(404, "Comment not found.")

        comment.content = dto.content
        db.commit()
        db.refresh(comment)

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Comment updated successfully.",
            data=CommentDTO.model_validate(comment),
        )
    except Exception as e:
        handle_exception(e, db)


def delete_comment_service(
    comment_id: int, db: Session
) -> BaseResponseDTO[None]:
    try:
        comment = (
            db.query(Comment).filter(Comment.comment_id == comment_id).first()
        )
        if not comment:
            raise CustomException(404, "Comment not found.")

        db.delete(comment)
        db.commit()

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Comment deleted successfully.",
            data=None,
        )
    except Exception as e:
        handle_exception(e, db)
