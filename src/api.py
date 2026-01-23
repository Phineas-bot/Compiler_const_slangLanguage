from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyzer import Lexer, parse_sentence


app = FastAPI(title="Yaounde Slang Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)


class CheckRequest(BaseModel):
    sentence: str
    explain: bool = True
    tokens: bool = True


class CheckResponse(BaseModel):
    ok: bool
    diagnostic: Optional[Dict[str, Any]] = None
    tokens: Optional[List[List[str]]] = None
    actions: Optional[List[str]] = None
    stack: Optional[List[List[str]]] = None


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/check", response_model=CheckResponse)
def check(req: CheckRequest) -> CheckResponse:
    result = parse_sentence(req.sentence, explain=req.explain)
    response: Dict[str, Any] = {
        "ok": result["ok"],
        "diagnostic": result.get("diagnostic"),
        "actions": result.get("actions"),
        "stack": result.get("stack"),
    }

    if req.tokens:
        tokens = Lexer().tokenize(req.sentence)
        response["tokens"] = [[t[0], t[1]] for t in tokens]

    return CheckResponse(**response)
