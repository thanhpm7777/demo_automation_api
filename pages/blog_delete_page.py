"""
Page Object Model cho API DELETE /api/blogs/{id}/.

BlogDeletePage đóng gói tất cả request liên quan đến
endpoint xoá blog theo ID.
"""

import httpx
from configs.config import BASE_URL, BLOGS_ENDPOINT, REQUEST_TIMEOUT, NON_EXISTENT_ID, INVALID_STRING_ID


class BlogDeletePage:
    """
    POM class đại diện cho endpoint DELETE /api/blogs/{id}/.

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
    # Core method
    # ------------------------------------------------------------------

    def delete_blog(self, blog_id, headers: dict = None) -> httpx.Response:
        """
        Gửi DELETE request tới /api/blogs/{id}/.

        Args:
            blog_id: ID của blog cần xoá.
            headers: Headers bổ sung (VD: Authorization).

        Returns:
            httpx.Response object.
        """
        return self.client.delete(
            self._url(blog_id),
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def delete_non_existent_blog(self) -> httpx.Response:
        """DELETE blog với ID không tồn tại."""
        return self.delete_blog(NON_EXISTENT_ID)

    def delete_blog_by_string_id(self) -> httpx.Response:
        """DELETE blog với ID là chuỗi ký tự."""
        return self.delete_blog(INVALID_STRING_ID)
