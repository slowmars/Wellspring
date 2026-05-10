from fastapi import APIRouter, HTTPException
from ..schemas import LoginRequest, LoginResponse
from ..deps import VOLUNTEER_PW, STAFF_PW, make_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    if req.password == STAFF_PW:
        return LoginResponse(token=make_token("staff"), role="staff")
    elif req.password == VOLUNTEER_PW:
        return LoginResponse(token=make_token("volunteer"), role="volunteer")
    else:
        raise HTTPException(status_code=401, detail="Wrong password")
