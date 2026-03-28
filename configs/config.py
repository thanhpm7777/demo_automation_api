"""
Cấu hình chung cho toàn bộ test suite.
Bao gồm: endpoints, defaults, auth, performance thresholds.
"""

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
BASE_URL = "https://hocvancungricky.com"

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
BLOGS_ENDPOINT = "/api/blogs/"                    # GET list / POST
BLOG_DETAIL_ENDPOINT = "/api/blogs/{id}/"         # GET | PUT | PATCH | DELETE

# ---------------------------------------------------------------------------
# Giá trị mặc định của API
# ---------------------------------------------------------------------------
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

# ---------------------------------------------------------------------------
# Timeout & Performance thresholds (giây)
# ---------------------------------------------------------------------------
REQUEST_TIMEOUT = 10.0
MAX_RESPONSE_TIME = 3.0          # GET list
MAX_RESPONSE_TIME_DETAIL = 1.0   # GET by ID
MAX_RESPONSE_TIME_POST = 2.0     # POST create

# ---------------------------------------------------------------------------
# IDs dùng cho test
# ---------------------------------------------------------------------------
NON_EXISTENT_ID = 999999         # ID chắc chắn không tồn tại
INVALID_STRING_ID = "abc"        # ID không hợp lệ (chuỗi)

# ---------------------------------------------------------------------------
# Authentication (điền token thật nếu có)
# Để rỗng → các security test sẽ kiểm tra server trả 401/403
# ---------------------------------------------------------------------------
AUTH_TOKEN = ""                  # VD: "Token abcdef123456"

# ---------------------------------------------------------------------------
# Performance: concurrent request count
# ---------------------------------------------------------------------------
CONCURRENT_REQUESTS = 10
