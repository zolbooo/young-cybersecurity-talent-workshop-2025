from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
from typing import Dict, Any

app = FastAPI(title="Insecure JWT Demo")


class TokenPayload(BaseModel):
    token: str


def decode_none_alg_jwt(token: str) -> Dict[str, Any]:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token header: {e}")

    alg = header.get("alg")
    if alg != "none":
        # For demonstration, we only accept tokens explicitly using alg=none
        raise HTTPException(
            status_code=400, detail="Only JWTs with alg=none are accepted"
        )

    try:
        # PyJWT rejects alg=none by default. We manually parse parts and return payload unverified.
        # token format: header.payload.signature (signature expected empty)
        parts = token.split(".")
        if len(parts) != 3:
            raise HTTPException(status_code=400, detail="Malformed JWT")

        # Decode payload without verification
        payload = jwt.api_jwt.decode_complete(
            token, options={"verify_signature": False}
        )["payload"]
        return payload
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {e}")


@app.post("/login")
async def login(body: TokenPayload):
    payload = decode_none_alg_jwt(body.token)
    return {
        "accepted": True,
        "payload": payload,
        "flag": (
            "flag{insecure_jwt_demo}"
            if payload.get("user") == "admin"
            else "You are not an admin."
        ),
    }


@app.get("/")
async def root():
    return {"message": "Please refer to /docs for API documentation."}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
