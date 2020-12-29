from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from .core.expections import NotionException
from .routers import go, github
from .templates.not_found_template import (
    get_ticket_not_found_html,
    get_project_not_found_html,
)

app = FastAPI()

app.include_router(go.router)
app.include_router(github.router)


@app.get("/")
async def root():
    return "Hello Bigger Applications!"


@app.exception_handler(NotionException)
async def notion_exception_handler(request: Request, exc: NotionException):
    return HTMLResponse(
        status_code=404,
        content=exc.is_ticket
        and get_ticket_not_found_html(
            redirect_url=exc.redirect_to,
            ticket_id=exc.code,
        )
        or get_project_not_found_html(
            redirect_url=exc.redirect_to,
            prefix_id=exc.code,
        ),
    )
