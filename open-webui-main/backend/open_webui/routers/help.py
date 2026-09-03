from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()

# 系统帮助文档：case01 生成的项目说明文档（项目根目录）
HELP_DOC_PATH = Path(__file__).resolve().parents[3] / 'PROJECT_ARCHITECTURE.md'


@router.get('/document')
async def get_help_document(user=Depends(get_verified_user)):
    """返回系统帮助文档（Markdown），供前端帮助页展示。"""
    if not HELP_DOC_PATH.exists():
        raise HTTPException(status_code=404, detail='Help document not found')

    content = HELP_DOC_PATH.read_text(encoding='utf-8')
    first_line = next((ln for ln in content.splitlines() if ln.strip()), '')
    title = first_line.lstrip('#').strip() or 'Help'

    return {
        'title': title,
        'content': content,
        'source': HELP_DOC_PATH.name,
        'updated_at': HELP_DOC_PATH.stat().st_mtime,
    }
