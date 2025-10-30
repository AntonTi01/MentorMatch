from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from .db import get_conn
from .router import create_admin_router

load_dotenv()

app = FastAPI(title='MentorMatch Admin Service')
templates = Jinja2Templates(directory=os.path.dirname(__file__))
app.include_router(create_admin_router(get_conn, templates))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('admin.main:app', host='0.0.0.0', port=int(os.getenv('PORT', '8100')), reload=False)
