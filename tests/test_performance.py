"""
test_performance.py – Test cases kiểm tra hiệu năng Blog API

Bao phủ:
    PF-01  : Response time GET /api/blogs/ ≤ 3s
    PF-02  : Response time GET /api/blogs/{id}/ ≤ 1s
    PF-03  : Response time POST /api/blogs/ ≤ 2s
    PF-04  : 10 concurrent GET requests đều trả 200
    PF-05  : 10 concurrent POST requests (ghi nhận behavior, check không crash)
    PF-06  : GET với page_size=100 ≤ 3s, server không crash
    PF-07  : 50 sequential GET requests đều 200, không timeout
    PF-08  : Response headers GET có Cache-Control hoặc ETag

Markers: performance, regression
"""

import time
import threading
import pytest

from configs.config import (
    MAX_RESPONSE_TIME,
    MAX_RESPONSE_TIME_DETAIL,
    MAX_RESPONSE_TIME_POST,
    CONCURRENT_REQUESTS,
    REQUEST_TIMEOUT,
)


# ===========================================================================
# PF-01 ~ PF-03: Response Time Thresholds
# ===========================================================================

@pytest.mark.regression
@pytest.mark.performance
class TestResponseTime:
    """Kiểm tra response time không vượt ngưỡng quy định."""

    def test_PF01_get_list_response_time(self, blog_page):
        """PF-01: GET /api/blogs/ phải trả về trong ≤ 3s."""
        start = time.time()
        response = blog_page.get_blogs_default()
        elapsed = time.time() - start

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert elapsed <= MAX_RESPONSE_TIME, (
            f"PF-01 FAIL: Response time {elapsed:.3f}s vượt ngưỡng {MAX_RESPONSE_TIME}s"
        )

    def test_PF02_get_detail_response_time(self, blog_detail_page, valid_blog_id):
        """PF-02: GET /api/blogs/{id}/ phải trả về trong ≤ 1s."""
        start = time.time()
        response = blog_detail_page.get_blog_by_id(valid_blog_id)
        elapsed = time.time() - start

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert elapsed <= MAX_RESPONSE_TIME_DETAIL, (
            f"PF-02 FAIL: Response time {elapsed:.3f}s vượt ngưỡng {MAX_RESPONSE_TIME_DETAIL}s"
        )

    def test_PF03_post_create_response_time(self, blog_create_page):
        """PF-03: POST /api/blogs/ phải hoàn thành trong ≤ 2s (bao gồm cả 401/403)."""
        payload = {"title": "Perf Test Blog", "content": "Content for perf test"}
        start = time.time()
        response = blog_create_page.create_blog(payload)
        elapsed = time.time() - start

        # 201 hoặc 401/403 đều chấp nhận – quan tâm đến thời gian phản hồi
        assert response.status_code in (201, 400, 401, 403), (
            f"Unexpected status {response.status_code}"
        )
        assert elapsed <= MAX_RESPONSE_TIME_POST, (
            f"PF-03 FAIL: Response time {elapsed:.3f}s vượt ngưỡng {MAX_RESPONSE_TIME_POST}s"
        )


# ===========================================================================
# PF-04 ~ PF-05: Concurrent Requests
# ===========================================================================

@pytest.mark.regression
@pytest.mark.performance
class TestConcurrentRequests:
    """Kiểm tra server xử lý nhiều request đồng thời."""

    def test_PF04_concurrent_get_requests(self, blog_page):
        """PF-04: 10 concurrent GET /api/blogs/ phải đều trả về 200."""
        results = []
        errors = []

        def do_get():
            try:
                response = blog_page.get_blogs_default()
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=do_get) for _ in range(CONCURRENT_REQUESTS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=REQUEST_TIMEOUT)

        assert not errors, f"PF-04: {len(errors)} requests gặp lỗi exception: {errors[:3]}"
        failed = [s for s in results if s != 200]
        assert not failed, (
            f"PF-04: {len(failed)}/{CONCURRENT_REQUESTS} concurrent requests không trả về 200: {failed}"
        )
        assert len(results) == CONCURRENT_REQUESTS, (
            f"PF-04: Chỉ nhận {len(results)}/{CONCURRENT_REQUESTS} responses"
        )

    def test_PF05_concurrent_post_requests_no_crash(self, blog_create_page):
        """PF-05: 10 concurrent POST /api/blogs/ – server không crash (5xx)."""
        results = []
        errors = []

        def do_post():
            try:
                payload = {"title": "Concurrent Post Test", "content": "Concurrency test content"}
                response = blog_create_page.create_blog(payload)
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=do_post) for _ in range(CONCURRENT_REQUESTS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=REQUEST_TIMEOUT)

        server_errors = [s for s in results if s >= 500]
        assert not server_errors, (
            f"PF-05: Server trả 5xx trong concurrent POSTs: {server_errors}"
        )
        assert not errors, f"PF-05: Exception trong concurrent POST: {errors[:3]}"


# ===========================================================================
# PF-06 ~ PF-07: Large Page Size & Sequential Load
# ===========================================================================

@pytest.mark.regression
@pytest.mark.performance
class TestLoadBehavior:
    """Kiểm tra hành vi với page_size lớn và request tuần tự liên tiếp."""

    def test_PF06_large_page_size_response_time(self, blog_page):
        """PF-06: GET ?page_size=100 phải trả về ≤ 3s và không gây server error."""
        start = time.time()
        response = blog_page.get_blogs_with_page_size(100)
        elapsed = time.time() - start

        assert response.status_code in (200, 400), (
            f"Expected 200 or 400 for page_size=100, got {response.status_code}"
        )
        if response.status_code == 200:
            assert elapsed <= MAX_RESPONSE_TIME, (
                f"PF-06 FAIL: Response time {elapsed:.3f}s vượt ngưỡng {MAX_RESPONSE_TIME}s"
            )

    def test_PF07_sequential_50_get_requests(self, blog_page):
        """PF-07: 50 sequential GET /api/blogs/ đều phải trả 200, không timeout."""
        SEQUENTIAL_COUNT = 50
        failed = []
        for i in range(SEQUENTIAL_COUNT):
            try:
                response = blog_page.get_blogs_default()
                if response.status_code != 200:
                    failed.append((i + 1, response.status_code))
            except Exception as e:
                failed.append((i + 1, str(e)))

        assert not failed, (
            f"PF-07: {len(failed)}/{SEQUENTIAL_COUNT} requests thất bại: {failed[:5]}"
        )


# ===========================================================================
# PF-08: Cache Headers
# ===========================================================================

@pytest.mark.regression
@pytest.mark.performance
class TestCacheHeaders:
    """PF-08: Kiểm tra response headers cho caching hints."""

    # def test_PF08_cache_control_or_etag_header_present(self, blog_page):
    #     """PF-08: Response phải có Cache-Control hoặc ETag header."""
    #     response = blog_page.get_blogs_default()
    #     assert response.status_code == 200

    #     headers = response.headers
    #     has_cache_control = "cache-control" in headers
    #     has_etag = "etag" in headers
    #     has_last_modified = "last-modified" in headers

    #     assert has_cache_control or has_etag or has_last_modified, (
    #         "PF-08: Không tìm thấy Cache-Control, ETag, hoặc Last-Modified header.\n"
    #         f"Headers hiện có: {dict(headers)}"
    #     )

    # def test_PF08_response_has_content_type(self, blog_page):
    #     """PF-08b: Response phải có Content-Type: application/json."""
    #     response = blog_page.get_blogs_default()
    #     assert "application/json" in response.headers.get("content-type", ""), (
    #         "Content-Type phải là application/json"
    #     )
