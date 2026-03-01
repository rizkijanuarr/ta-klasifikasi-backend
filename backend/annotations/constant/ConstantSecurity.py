class ConstantSecurity:
    SECRET = "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970"
    EXPIRATION_TIME = 1000 * 60 * 15  # 15 minutes
    REFRESH_EXPIRATION_TIME = 1000 * 60 * 60 * 24 * 7  # 7 days
    EXPIRATION_TIME_GOOGLE = 86400000L * 7  # Expired OAuth Google
    BEARER_TOKEN_PREFIX = "Bearer "  # Prefix di Authorization header
    BASIC_TOKEN_PREFIX = "Basic "  # Prefix basic auth
    SIGN_UP_URL = "/users/sign-up"  # Endpoint signup
    NAME_APP = "Tugas Akhir: Sistem Klasifikasi Website Legal / Ilegal"  # Nama aplikasi