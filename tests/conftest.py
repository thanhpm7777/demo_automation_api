"""
conftest.py – Fixtures dùng chung cho toàn bộ test suite.

Fixtures:
    client          : httpx.Client được khởi tạo 1 lần mỗi session.
    blog_page       : Instance của BlogListPage dùng chung.
    blog_detail_page: Instance của BlogDetailPage dùng chung.
    blog_create_page: Instance của BlogCreatePage dùng chung.
    blog_update_page: Instance của BlogUpdatePage dùng chung.
    blog_delete_page: Instance của BlogDeletePage dùng chung.
    valid_blog_id   : ID hợp lệ lấy từ GET /api/blogs/ results[0].
    default_response: Response mặc định GET /api/blogs/ (1 lần / module).
"""

import pytest
import httpx

from pages.blog_list_page import BlogListPage
from pages.blog_detail_page import BlogDetailPage
from pages.blog_create_page import BlogCreatePage
from pages.blog_update_page import BlogUpdatePage
from pages.blog_delete_page import BlogDeletePage
from configs.config import BASE_URL, AUTH_TOKEN


# ---------------------------------------------------------------------------
# HTTP Client
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def client():
    """
    Tạo httpx.Client dùng chung cho toàn session.
    base_url giúp rút ngắn URL khi gọi trong các page object.
    """
    with httpx.Client(base_url=BASE_URL) as c:
        yield c


# ---------------------------------------------------------------------------
# Page Object fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def blog_page(client):
    """Trả về instance BlogListPage dùng chung cho toàn session."""
    return BlogListPage(client)


@pytest.fixture(scope="session")
def blog_detail_page(client):
    """Trả về instance BlogDetailPage dùng chung cho toàn session."""
    return BlogDetailPage(client)


@pytest.fixture(scope="session")
def blog_create_page(client):
    """Trả về instance BlogCreatePage dùng chung cho toàn session."""
    return BlogCreatePage(client)


@pytest.fixture(scope="session")
def blog_update_page(client):
    """Trả về instance BlogUpdatePage dùng chung cho toàn session."""
    return BlogUpdatePage(client)


@pytest.fixture(scope="session")
def blog_delete_page(client):
    """Trả về instance BlogDeletePage dùng chung cho toàn session."""
    return BlogDeletePage(client)


# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def valid_blog_id(blog_page):
    """
    Lấy ID hợp lệ từ results[0] của GET /api/blogs/.
    Dùng chung cho GET detail, PUT, PATCH tests.
    """
    response = blog_page.get_blogs_default()
    assert response.status_code == 200, "Không lấy được danh sách blogs để lấy valid_blog_id"
    results = response.json().get("results", [])
    assert results, "results rỗng – không thể xác định valid_blog_id"
    return results[0]["id"]


@pytest.fixture(scope="session")
def auth_headers():
    """
    Headers chứa token xác thực.
    Nếu AUTH_TOKEN rỗng → trả về {} (dùng để test unauthenticated).
    """
    if AUTH_TOKEN:
        return {"Authorization": AUTH_TOKEN}
    return {}


@pytest.fixture(scope="session")
def no_auth_headers():
    """Headers không có Authorization – dùng cho security tests."""
    return {}


# ---------------------------------------------------------------------------
# Shared response fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def default_response(blog_page):
    """
    Gọi GET /api/blogs/ mặc định 1 lần cho cả module,
    tránh gọi lặp nhiều lần trong các test cùng kiểm tra response body.
    """
    return blog_page.get_blogs_default()
