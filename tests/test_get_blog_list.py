"""
test_get_blog_list.py - Bo testcase cho API GET /api/blogs/
Thiet ke theo mo hinh POM su dung pytest + httpx.

API: GET https://hocvancungricky.com/api/blogs/
Supported query params: ?page, ?page_size, ?search

Markers:
    smoke      - TC01, TC02, TC03, TC09, TC22 (chuc nang cot loi)
    regression - Toan bo 22 TC

Cach chay:
    pytest -m smoke          # chi chay smoke (5 TC)
    pytest -m regression     # chay toan bo (22 TC)
"""

import time
import pytest

from configs.config import DEFAULT_PAGE_SIZE, MAX_RESPONSE_TIME

# ---------------------------------------------------------------------------
# Cac field bat buoc o cap response va cap blog item
# ---------------------------------------------------------------------------

REQUIRED_RESPONSE_FIELDS = {"count", "page", "page_size", "next", "previous", "results"}

REQUIRED_BLOG_FIELDS = {
    "id",
    "title",
    "slug",
    "created_date",
    "updated_date",
    "view_count",
    "like_count",
    "is_active",
    "banner_url",
    "user",
    "category",
    "tags",
}


# ===========================================================================
# TC01 - TC08: Kiem tra response mac dinh (khong params)
# ===========================================================================


@pytest.mark.regression
class TestDefaultResponse:
    """Nhom test dung chung fixture default_response (goi API 1 lan / module)."""

    @pytest.mark.smoke
    def test_TC01_get_blogs_status_200(self, default_response):
        """TC01: GET /api/blogs/ phai tra ve HTTP 200 OK."""
        assert default_response.status_code == 200, (
            f"Expected 200, got {default_response.status_code}"
        )

    @pytest.mark.smoke
    def test_TC02_response_is_json(self, default_response):
        """TC02: Content-Type phai chua 'application/json'."""
        content_type = default_response.headers.get("content-type", "")
        assert "application/json" in content_type, (
            f"Expected application/json, got: {content_type}"
        )

    @pytest.mark.smoke
    def test_TC03_response_has_required_fields(self, default_response):
        """TC03: Response body phai co du cac field: count, page, page_size, next, previous, results."""
        body = default_response.json()
        missing = REQUIRED_RESPONSE_FIELDS - body.keys()
        assert not missing, f"Thieu field: {missing}"

    def test_TC04_default_page_is_1(self, default_response):
        """TC04: Gia tri page mac dinh phai la 1."""
        body = default_response.json()
        assert body["page"] == 1, f"Expected page=1, got {body['page']}"

    def test_TC05_default_page_size_is_10(self, default_response):
        """TC05: page_size mac dinh phai la 10 va len(results) cung phai la 10."""
        body = default_response.json()
        assert body["page_size"] == DEFAULT_PAGE_SIZE, (
            f"Expected page_size={DEFAULT_PAGE_SIZE}, got {body['page_size']}"
        )
        assert len(body["results"]) == DEFAULT_PAGE_SIZE, (
            f"Expected {DEFAULT_PAGE_SIZE} items, got {len(body['results'])}"
        )

    def test_TC06_count_is_positive_integer(self, default_response):
        """TC06: count phai la so nguyen duong (> 0)."""
        body = default_response.json()
        assert isinstance(body["count"], int), "count phai la integer"
        assert body["count"] > 0, f"count phai > 0, got {body['count']}"

    def test_TC07_previous_is_null_on_page_1(self, default_response):
        """TC07: previous phai la null o trang dau tien."""
        body = default_response.json()
        assert body["previous"] is None, (
            f"Expected previous=null, got {body['previous']}"
        )

    def test_TC08_next_is_not_null_on_page_1(self, default_response):
        """TC08: next khong duoc null khi tong so trang > 1."""
        body = default_response.json()
        if body["count"] > body["page_size"]:
            assert body["next"] is not None, "next phai co gia tri khi co nhieu trang"


# ===========================================================================
# TC09 - TC13: Kiem tra cau truc tung blog item
# ===========================================================================


@pytest.mark.regression
class TestBlogItemStructure:
    """Kiem tra schema cua tung phan tu trong results[]."""

    @pytest.mark.smoke
    def test_TC09_blog_item_required_fields(self, default_response):
        """TC09: Moi blog item phai co du field bat buoc."""
        results = default_response.json()["results"]
        assert results, "results khong duoc rong"
        for blog in results:
            missing = REQUIRED_BLOG_FIELDS - blog.keys()
            assert not missing, f"Blog id={blog.get('id')} thieu field: {missing}"

    def test_TC10_blog_item_field_types(self, default_response):
        """TC10: Kiem tra kieu du lieu cua cac field trong blog item."""
        results = default_response.json()["results"]
        for blog in results:
            bid = blog.get("id")
            assert isinstance(blog["id"], int), f"[id={bid}] id phai la int"
            assert isinstance(blog["title"], str), f"[id={bid}] title phai la str"
            assert isinstance(blog["slug"], str), f"[id={bid}] slug phai la str"
            assert isinstance(blog["created_date"], str), f"[id={bid}] created_date phai la str"
            assert isinstance(blog["updated_date"], str), f"[id={bid}] updated_date phai la str"
            assert isinstance(blog["view_count"], int), f"[id={bid}] view_count phai la int"
            assert isinstance(blog["like_count"], int), f"[id={bid}] like_count phai la int"
            assert isinstance(blog["is_active"], bool), f"[id={bid}] is_active phai la bool"
            assert isinstance(blog["banner_url"], str), f"[id={bid}] banner_url phai la str"

    def test_TC11_user_object_structure(self, default_response):
        """TC11: Moi blog item phai co user.id (int) va user.username (str)."""
        results = default_response.json()["results"]
        for blog in results:
            user = blog["user"]
            bid = blog.get("id")
            assert isinstance(user, dict), f"[id={bid}] user phai la object"
            assert "id" in user, f"[id={bid}] user thieu field 'id'"
            assert "username" in user, f"[id={bid}] user thieu field 'username'"
            assert isinstance(user["id"], int), f"[id={bid}] user.id phai la int"
            assert isinstance(user["username"], str), f"[id={bid}] user.username phai la str"

    def test_TC12_category_object_structure(self, default_response):
        """TC12: Moi blog item phai co category.id (int), category.title (str), category.slug (str)."""
        results = default_response.json()["results"]
        for blog in results:
            category = blog["category"]
            bid = blog.get("id")
            assert isinstance(category, dict), f"[id={bid}] category phai la object"
            assert "id" in category, f"[id={bid}] category thieu 'id'"
            assert "title" in category, f"[id={bid}] category thieu 'title'"
            assert "slug" in category, f"[id={bid}] category thieu 'slug'"
            assert isinstance(category["id"], int), f"[id={bid}] category.id phai la int"
            assert isinstance(category["title"], str), f"[id={bid}] category.title phai la str"
            assert isinstance(category["slug"], str), f"[id={bid}] category.slug phai la str"

    def test_TC13_tags_is_list(self, default_response):
        """TC13: tags phai la danh sach (list) trong moi blog item."""
        results = default_response.json()["results"]
        for blog in results:
            bid = blog.get("id")
            assert isinstance(blog["tags"], list), f"[id={bid}] tags phai la list"


# ===========================================================================
# TC14 - TC17: Kiem tra phan trang (pagination)
# ===========================================================================


@pytest.mark.regression
class TestPagination:
    """Nhom test kiem tra cac tham so phan trang: ?page, ?page_size."""

    def test_TC14_pagination_page_2(self, blog_page):
        """TC14: ?page=2 phai tra ve page=2 va previous khong null."""
        response = blog_page.get_blogs_with_page(2)
        assert response.status_code == 200
        body = response.json()
        assert body["page"] == 2, f"Expected page=2, got {body['page']}"
        assert body["previous"] is not None, "previous phai khong null o page 2"

    def test_TC15_custom_page_size_5(self, blog_page):
        """TC15: ?page_size=5 phai tra ve page_size=5 va len(results)==5."""
        response = blog_page.get_blogs_with_page_size(5)
        assert response.status_code == 200
        body = response.json()
        assert body["page_size"] == 5, f"Expected page_size=5, got {body['page_size']}"
        assert len(body["results"]) == 5, f"Expected 5 items, got {len(body['results'])}"

    def test_TC16_page_and_page_size_combined(self, blog_page):
        """TC16: ?page=2&page_size=5 phai tra ve page=2, page_size=5, len(results)==5."""
        response = blog_page.get_blogs_with_page_and_size(page=2, page_size=5)
        assert response.status_code == 200
        body = response.json()
        assert body["page"] == 2, f"Expected page=2, got {body['page']}"
        assert body["page_size"] == 5, f"Expected page_size=5, got {body['page_size']}"
        assert len(body["results"]) == 5, f"Expected 5 items, got {len(body['results'])}"

    def test_TC17_out_of_range_page_returns_last_page(self, blog_page):
        """TC17: ?page=999 (vuot qua gioi han) phai tra ve trang cuoi hop le voi next=null."""
        response = blog_page.get_blogs_with_page(999)
        assert response.status_code == 200
        body = response.json()
        assert body["next"] is None, "next phai null o trang cuoi"
        assert len(body["results"]) > 0, "results khong duoc rong du page vuot gioi han"


# ===========================================================================
# TC18 - TC20: Kiem tra tim kiem (search)
# ===========================================================================


@pytest.mark.regression
class TestSearch:
    """Nhom test kiem tra tham so ?search."""

    def test_TC18_search_returns_filtered_results(self, blog_page):
        """TC18: ?search=van phai tra ve it ket qua hon tong so blogs."""
        total_response = blog_page.get_blogs_default()
        total_count = total_response.json()["count"]

        search_response = blog_page.get_blogs_with_search("van")
        assert search_response.status_code == 200
        search_body = search_response.json()
        assert search_body["count"] < total_count, (
            f"Ket qua search phai nho hon total. search_count={search_body['count']}, total={total_count}"
        )

    def test_TC19_search_empty_keyword(self, blog_page):
        """TC19: ?search= (rong) phai tra ve 200 va results hop le."""
        response = blog_page.get_blogs_with_search("")
        assert response.status_code == 200
        body = response.json()
        assert "results" in body
        assert isinstance(body["results"], list)

    def test_TC20_search_no_match(self, blog_page):
        """TC20: ?search=xyz123notexist phai tra ve count=0 hoac results rong."""
        response = blog_page.get_blogs_with_search("xyzxyz123notexist")
        assert response.status_code == 200
        body = response.json()
        assert body["count"] == 0 or len(body["results"]) == 0, (
            f"Expected empty results, got count={body['count']}, results={len(body['results'])}"
        )


# ===========================================================================
# TC21 - TC22: Kiem tra dinh dang va hieu nang
# ===========================================================================


@pytest.mark.regression
class TestFormatAndPerformance:
    """Nhom test kiem tra dinh dang URL va thoi gian phan hoi."""

    def test_TC21_next_url_is_valid_format(self, default_response):
        """TC21: URL next phai co dinh dang hop le, chua ?page=2."""
        body = default_response.json()
        next_url = body.get("next")
        if next_url is not None:
            assert "page=2" in next_url, (
                f"next URL phai chua 'page=2', got: {next_url}"
            )
            assert next_url.startswith("http"), (
                f"next URL phai bat dau bang 'http', got: {next_url}"
            )

    @pytest.mark.smoke
    def test_TC22_response_time_under_3s(self, blog_page):
        """TC22: Thoi gian phan hoi cua GET /api/blogs/ phai duoi 3 giay."""
        start = time.time()
        response = blog_page.get_blogs_default()
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < MAX_RESPONSE_TIME, (
            f"Response time {elapsed:.2f}s vuot nguong {MAX_RESPONSE_TIME}s"
        )
