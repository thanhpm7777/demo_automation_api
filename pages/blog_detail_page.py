"""
Page Object Model cho API GET /api/blogs/{id}/.

BlogDetailPage đóng gói tất cả request liên quan đến
endpoint lấy chi tiết một blog theo ID.
"""

import httpx
from configs.config import BASE_URL, BLOGS_ENDPOINT, REQUEST_TIMEOUT


class BlogDetailPage:
    """
    POM class đại diện cho endpoint GET /api/blogs/{id}/.

    Attributes:
        client (httpx.Client): HTTP client dùng chung.
        base_endpoint (str): URL gốc của endpoint blogs.
    """

    def __init__(self, client: httpx.Client):
        self.client = client
        self.base_endpoint = f"{BASE_URL}{BLOGS_ENDPOINT}"

    def _url(self, blog_id) -> str:
        """Tạo URL đầy đủ cho một blog ID."""
        return f"{self.base_endpoint}{blog_id}/"

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------

    def get_blog_by_id(self, blog_id: int, headers: dict = None) -> httpx.Response:
        """
        Gửi GET request tới /api/blogs/{id}/.

        Args:
            blog_id: ID của blog cần lấy.
            headers: Headers bổ sung (VD: Authorization).

        Returns:
            httpx.Response object.
        """
        return self.client.get(
            self._url(blog_id),
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    def get_blog_by_string_id(self, string_id: str) -> httpx.Response:
        """Gửi GET request với ID là chuỗi không hợp lệ."""
        return self.client.get(
            self._url(string_id),
            timeout=REQUEST_TIMEOUT,
        )
