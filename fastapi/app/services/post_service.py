from sqlalchemy.orm import Session, joinedload
from entities.post import Post
from entities.crop import Crop
from exception import CustomException, handle_exception
from dtos.base_dto import BaseResponseDTO
from dtos.post_dto import (
    AddPostRequestDTO,
    UpdatePostRequestDTO,
    GetPostListRequestDTO,
    GetPostListResponseDTO,
    GetPostDetailResponseDTO,
    PostDTO,
    PostDetailDTO,
)


def get_post_detail_service(
    post_id: int, db: Session
) -> GetPostDetailResponseDTO:
    try:
        post = (
            db.query(Post)
            .options(joinedload(Post.comments))  # 댓글 포함
            .filter(Post.post_id == post_id)
            .first()
        )

        if not post:
            raise CustomException(404, "Post not found.")

        return GetPostDetailResponseDTO(
            success=True,
            code=200,
            message="Post detail retrieved successfully.",
            data=PostDetailDTO.model_validate(post),
        )
    except Exception as e:
        handle_exception(e, db)


def add_post_service(
    dto: AddPostRequestDTO, db: Session
) -> GetPostDetailResponseDTO:
    try:
        crop = db.query(Crop).filter(Crop.crop_id == dto.crop_id).first()
        if not crop:
            raise CustomException(404, "Crop not found.")

        post = Post(crop_id=dto.crop_id, title=dto.title, content=dto.content)
        db.add(post)
        db.commit()

        return get_post_detail_service(post.post_id, db)
    except Exception as e:
        handle_exception(e, db)


def get_post_list_service(
    dto: GetPostListRequestDTO, db: Session
) -> GetPostListResponseDTO:
    try:
        query = db.query(Post).join(Post.crop)

        if dto.group_id:
            query = query.filter(Crop.group_id == dto.group_id)
        if dto.crop_id:
            query = query.filter(Post.crop_id == dto.crop_id)

        posts = query.all()
        post_dtos = [PostDTO.model_validate(post) for post in posts]

        return GetPostListResponseDTO(
            success=True,
            code=200,
            message="Post list retrieved successfully.",
            data=post_dtos,
        )
    except Exception as e:
        handle_exception(e, db)


def update_post_service(
    post_id: int, dto: UpdatePostRequestDTO, db: Session
) -> GetPostDetailResponseDTO:
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise CustomException(404, "Post not found.")

        for key, value in dto.model_dump(exclude_unset=True).items():
            setattr(post, key, value)

        db.commit()

        return get_post_detail_service(post.post_id, db)
    except Exception as e:
        handle_exception(e, db)


def delete_post_service(post_id: int, db: Session) -> BaseResponseDTO[None]:
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise CustomException(404, "Post not found.")

        db.delete(post)
        db.commit()

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Post deleted successfully.",
            data=None,
        )
    except Exception as e:
        handle_exception(e, db)
