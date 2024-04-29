from fastapi import APIRouter, HTTPException
from storeapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


post_table = {}
comment_table = {}


# Untuk menemukan post berdasarkan id
def find_post(post_id: int):
    return post_table.get(post_id)


# Untuk
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_reord_id = len(post_table)
    new_post = {**data, "id": last_reord_id}
    post_table[last_reord_id] = new_post
    return new_post


# Untuk mendapatkan semua post
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


# Route to post a comment
@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    # Error handling
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


# Route to get all comment on a post berdasarkan id post
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]

    # Pastikan untuk membangun respons yang sesuai dengan struktur yang diharapkan.
    return UserPostWithComments(post=UserPost(**post), comments=comments)
