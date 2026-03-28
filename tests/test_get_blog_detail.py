"""
test_get_blog_detail.py – Test cases cho API GET /api/blogs/{id}/

Bao phủ:
    HP-03 : GET blog hợp lệ → 200, đầy đủ fields
    NT-01 : GET ID không tồn tại → 404
    NT-10 : GET ID là chuỗi ký tự → 404/400
    EC-12 : GET blog đã bị xoá → 404

Markers: regression, smoke, happy_path, negative, edge
"""

import pytest


# ---------------------------------------------------------------------------
# Fields bắt buộc của một blog detail item
# ---------------------------------------------------------------------------
REQUIRED_DETAIL_FIELDS = {"id", "title", "slug", "created_date", "updated_date",
                           "view_count", "like_count", "is_active", "banner_url", "user",
                           "category", "tags"}


# ===========================================================================
# Happy Path
# ===========================================================================

@pytest.mark.regression
@pytest.mark.happy_path
class TestGetBlogDetailHappyPath:
    """HP-03: Lấy chi tiết blog theo ID hợp lệ."""

    @pytest.mark.smoke
    def test_HP03_get_detail_status_200(self, blog_detail_page, valid_blog_id):
        """HP-03a: GET /api/blogs/{valid_id}/ phải trả về 200."""
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. ID={valid_blog_id}"
        )

    def test_HP03_get_detail_content_type_json(self, blog_detail_page, valid_blog_id):
        """HP-03b: Content-Type phải là application/json."""
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        assert "application/json" in response.headers.get("content-type", "")

    def test_HP03_get_detail_required_fields(self, blog_detail_page, valid_blog_id):
        """HP-03c: Response phải có đủ các field bắt buộc."""
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        body = response.json()
        missing = REQUIRED_DETAIL_FIELDS - body.keys()
        assert not missing, f"Thiếu các field: {missing}"

    def test_HP03_get_detail_id_matches(self, blog_detail_page, valid_blog_id):
        """HP-03d: ID trong response phải khớp với ID yêu cầu."""
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        body = response.json()
        assert body["id"] == valid_blog_id, (
            f"Expected id={valid_blog_id}, got {body['id']}"
        )

    def test_HP03_get_detail_field_types(self, blog_detail_page, valid_blog_id):
        """HP-03e: Kiểm tra kiểu dữ liệu các field trong response."""
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        body = response.json()
        assert isinstance(body["id"], int), "id phải là int"
        assert isinstance(body["title"], str), "title phải là str"
        assert isinstance(body["slug"], str), "slug phải là str"
        assert isinstance(body["view_count"], int), "view_count phải là int"
        assert isinstance(body["like_count"], int), "like_count phải là int"
        assert isinstance(body["is_active"], bool), "is_active phải là bool"
        assert isinstance(body["tags"], list), "tags phải là list"
        assert isinstance(body["user"], dict), "user phải là dict"
        assert isinstance(body["category"], dict), "category phải là dict"


# ===========================================================================
# Negative Tests
# ===========================================================================

@pytest.mark.regression
@pytest.mark.negative
class TestGetBlogDetailNegative:
    """NT-01, NT-10: ID không tồn tại, ID là chuỗi ký tự."""

    def test_NT01_get_non_existent_id_returns_404(self, blog_detail_page):
        """NT-01: GET /api/blogs/999999/ phải trả về 404."""
        response = blog_detail_page.get_blog_by_id(999999)
        assert response.status_code == 404, (
            f"Expected 404, got {response.status_code}"
        )

    def test_NT01_get_non_existent_id_error_message(self, blog_detail_page):
        """NT-01b: Response body 404 phải có field 'detail'."""
        response = blog_detail_page.get_blog_by_id(999999)
        body = response.json()
        assert "detail" in body, f"Thiếu field 'detail' trong response 404: {body}"

    def test_NT10_get_string_id(self, blog_detail_page):
        """NT-10: GET /api/blogs/abc/ phải trả về 404 hoặc 400."""
        response = blog_detail_page.get_blog_by_string_id("abc")
        assert response.status_code in (400, 404), (
            f"Expected 400 or 404 for string ID, got {response.status_code}"
        )


# ===========================================================================
# Edge Cases
# ===========================================================================

@pytest.mark.regression
@pytest.mark.edge
class TestGetBlogDetailEdge:
    """EC-12: Truy cập blog đã bị xoá phải trả về 404."""

    def test_EC12_get_deleted_blog_returns_404(self, blog_detail_page):
        """EC-12: GET blog đã xoá → 404. Dùng NON_EXISTENT_ID để simulate."""
        response = blog_detail_page.get_blog_by_id(999999)
        assert response.status_code == 404, (
            f"Expected 404 for deleted/nonexistent blog, got {response.status_code}"
        )
