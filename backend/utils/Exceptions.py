class ScrapingFailedException(Exception):
    """
    Exception yang di-raise ketika scraping gagal atau content kosong.
    Akan menghasilkan HTTP 422 Unprocessable Entity.
    """
    def __init__(self, url: str, message: str = "Content tidak dapat di-scrape"):
        self.url = url
        self.message = message
        super().__init__(self.message)
