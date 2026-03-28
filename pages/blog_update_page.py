"""
Page Object Model cho API PUT/PATCH /api/blogs/{id}/.

BlogUpdatePage đóng gói tất cả request liên quan đến
endpoint cập nhật blog (toàn phần và một phần).
"""

import httpx
from configs.config import BASE_URL, BLOGS_ENDPOINT, REQUEST_TIMEOUT


class BlogUpdatePage:
    """
    POM class đại diện cho endpoint PUT/PATCH /api/blogs/{id}/.

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

    def put_blog(self, blog_id, payload: dict, headers: dict = None) -> httpx.Response:
        """
        Gửi PUT request tới /api/blogs/{id}/ — cập nhật toàn bộ.

        Args:
            blog_id: ID của blog cần cập nhật.
            payload: Dict đầy đủ các field cần cập nhật.
            headers: Headers bổ sung (VD: Authorization).

        Returns:
            httpx.Response object.
        """
        return self.client.put(
            self._url(blog_id),
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    def patch_blog(self, blog_id, payload: dict, headers: dict = None) -> httpx.Response:
        """
        Gửi PATCH request tới /api/blogs/{id}/ — cập nhật một phần.

        Args:
            blog_id: ID của blog cần cập nhật.
            payload: Dict chứa các field cần thay đổi.
            headers: Headers bổ sung (VD: Authorization).

        Returns:
            httpx.Response object.
        """
        return self.client.patch(
            self._url(blog_id),
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def put_blog_missing_required_fields(self, blog_id) -> httpx.Response:
        """PUT với payload thiếu field bắt buộc (chỉ có title)."""
        return self.put_blog(blog_id, {"title": "Only Title"})

    def put_blog_non_existent(self, payload: dict) -> httpx.Response:
        """PUT vào ID không tồn tại."""
        from configs.config import NON_EXISTENT_ID
        return self.put_blog(NON_EXISTENT_ID, payload)
