from fastapi import APIRouter
from storeapi.models.post import UserPost, UserPostIn

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


post_table = {}


@router.post("/post", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_reord_id = len(post_table)
    new_post = {**data, "id": last_reord_id}
    post_table[last_reord_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())
