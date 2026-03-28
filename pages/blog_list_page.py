"""
Page Object Model cho API GET /api/blogs/.

BlogListPage đóng gói tất cả các request liên quan đến
endpoint lấy danh sách blogs, giúp tách biệt logic gọi API
khỏi logic kiểm thử.
"""

import httpx
from configs.config import BASE_URL, BLOGS_ENDPOINT, REQUEST_TIMEOUT


class BlogListPage:
    """
    POM class đại diện cho endpoint GET /api/blogs/.

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

    def get_blogs(self, params: dict = None) -> httpx.Response:
        """
        Gửi GET request tới /api/blogs/ với các query params tùy chọn.

        Args:
            params: Dict query params, ví dụ {"page": 2, "page_size": 5}.

        Returns:
            httpx.Response object.
        """
        return self.client.get(
            self.endpoint,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

    # ------------------------------------------------------------------
    # Convenience methods (POM style)
    # ------------------------------------------------------------------

    def get_blogs_default(self) -> httpx.Response:
        """Lấy danh sách blogs với tham số mặc định (không truyền params)."""
        return self.get_blogs()

    def get_blogs_with_page(self, page: int) -> httpx.Response:
        """Lấy danh sách blogs theo số trang chỉ định."""
        return self.get_blogs(params={"page": page})

    def get_blogs_with_page_size(self, page_size: int) -> httpx.Response:
        """Lấy danh sách blogs với kích thước trang chỉ định."""
        return self.get_blogs(params={"page_size": page_size})

    def get_blogs_with_search(self, keyword: str) -> httpx.Response:
        """Tìm kiếm blogs theo từ khóa."""
        return self.get_blogs(params={"search": keyword})

    def get_blogs_with_page_and_size(
        self, page: int, page_size: int
    ) -> httpx.Response:
        """Lấy danh sách blogs với cả page lẫn page_size."""
        return self.get_blogs(params={"page": page, "page_size": page_size})
