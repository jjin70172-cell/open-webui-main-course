"""系统帮助文档接口测试（feature-development-workflow 步骤 5：先补测试）。

覆盖：
- 正常路径：返回 200 与文档内容
- 内容一致性：返回内容与源文件 PROJECT_ARCHITECTURE.md 完全一致
- 边界：文档文件缺失时返回 404
- 鉴权：未携带 token 时拒绝访问
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from open_webui.routers import help as help_router
from open_webui.utils.auth import get_verified_user


class DummyUser:
    id = 'test-user'
    role = 'user'
    email = 'test@example.com'


@pytest.fixture()
def client():
    app = FastAPI()
    app.include_router(help_router.router, prefix='/api/v1/help')
    app.dependency_overrides[get_verified_user] = lambda: DummyUser()
    return TestClient(app)


def test_get_help_document_returns_200_with_content(client):
    res = client.get('/api/v1/help/document')
    assert res.status_code == 200
    data = res.json()
    assert data['title']
    assert 'Open WebUI' in data['content']
    assert data['source'] == 'PROJECT_ARCHITECTURE.md'


def test_help_document_content_matches_source_file(client):
    res = client.get('/api/v1/help/document')
    expected = help_router.HELP_DOC_PATH.read_text(encoding='utf-8')
    assert res.json()['content'] == expected


def test_help_document_missing_returns_404(client, monkeypatch):
    monkeypatch.setattr(help_router, 'HELP_DOC_PATH', help_router.Path('/nonexistent/help.md'))
    res = client.get('/api/v1/help/document')
    assert res.status_code == 404


def test_help_document_requires_auth():
    app = FastAPI()
    app.include_router(help_router.router, prefix='/api/v1/help')
    c = TestClient(app)
    res = c.get('/api/v1/help/document')
    assert res.status_code in (401, 403)
