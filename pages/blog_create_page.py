"""
Page Object Model cho API POST /api/blogs/.

BlogCreatePage đóng gói tất cả request liên quan đến
endpoint tạo mới blog.
"""

import httpx
from configs.config import BASE_URL, BLOGS_ENDPOINT, REQUEST_TIMEOUT


class BlogCreatePage:
    """
    POM class đại diện cho endpoint POST /api/blogs/.

    Attributes:
        client (httpx.Client): HTTP client dùng chung.
        endpoint (str): Full URL của endpoint.
    """

    def __init__(self, client: httpx.Client):
        self.client = client
        self.endpoint = f"{BASE_URL}{BLOGS_ENDPOINT}"

    # ------------------------------------------------------------------
    # Core method
    # ------------------------------------------------------------------

    def create_blog(self, payload: dict, headers: dict = None) -> httpx.Response:
        """
        Gửi POST request tới /api/blogs/.

        Args:
            payload: Dict chứa dữ liệu blog (title, content, ...).
            headers: Headers bổ sung (VD: Authorization, Content-Type).

        Returns:
            httpx.Response object.
        """
        return self.client.post(
            self.endpoint,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    # ------------------------------------------------------------------
    # Convenience methods — Negative / Edge cases
    # ------------------------------------------------------------------

    def create_blog_missing_title(self, content: str = "Some content") -> httpx.Response:
        """POST thiếu field title bắt buộc."""
        return self.create_blog({"content": content})

    def create_blog_missing_content(self, title: str = "Some title") -> httpx.Response:
        """POST thiếu field content bắt buộc."""
        return self.create_blog({"title": title})

    def create_blog_empty_title(self, content: str = "Some content") -> httpx.Response:
        """POST với title là chuỗi rỗng."""
        return self.create_blog({"title": "", "content": content})

    def create_blog_whitespace_title(self, content: str = "Some content") -> httpx.Response:
        """POST với title toàn khoảng trắng."""
        return self.create_blog({"title": "   ", "content": content})

    def create_blog_wrong_author_type(self) -> httpx.Response:
        """POST với author là chuỗi (sai kiểu int)."""
        return self.create_blog({"title": "T", "content": "C", "author": "not_an_int"})

    def create_blog_with_xss(self) -> httpx.Response:
        """POST với XSS payload trong title."""
        return self.create_blog(
            {"title": "<script>alert('XSS')</script>", "content": "<img src=x onerror=alert(1)>"}
        )

    def create_blog_with_html(self) -> httpx.Response:
        """POST với HTML tags trong title."""
        return self.create_blog(
            {"title": "<b>Bold Title</b>", "content": "<p>Some content</p>"}
        )

    def create_blog_mass_assignment(self) -> httpx.Response:
        """POST với id trong body (mass assignment test)."""
        return self.create_blog({"id": 9999, "title": "Mass Test", "content": "Content"})

    def create_blog_with_wrong_content_type(self, raw_body: str = "plain text body") -> httpx.Response:
        """POST với Content-Type sai (text/plain)."""
        return self.client.post(
            self.endpoint,
            content=raw_body,
            headers={"Content-Type": "text/plain"},
            timeout=REQUEST_TIMEOUT,
        )

    def create_blog_with_plain_text_json(self, body: str = "this is not json") -> httpx.Response:
        """POST với body là text thô, không phải JSON."""
        return self.client.post(
            self.endpoint,
            content=body,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT,
        )
