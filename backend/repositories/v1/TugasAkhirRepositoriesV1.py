import re
import requests
import socket
from urllib.parse import urlparse
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import os
from datetime import datetime
import json
from backend.utils.ColoredLogger import setup_colored_logger
from backend.utils.Exceptions import ScrapingFailedException

# Setup colored logger
logger = setup_colored_logger(__name__)

class TugasAkhirRepositoriesV1:


    #-----------------------------------------------------------
    # VARIABLES
    #-----------------------------------------------------------
    _DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    # IndoBERT model reference (not loaded in production)
    _CALL_MODEL_INDOBERT = "indobenchmark/indobert-base-p2"
    _tokenizer = None
    _model = None

    _URL_PATTERN = re.compile(r"https?://\S+")
    _HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
    _MULTI_SPACE_PATTERN = re.compile(r"\s+")

    #-----------------------------------------------------------
    # CONSTRUCTOR
    #-----------------------------------------------------------
    def __init__(self):
        pass


    #-----------------------------------------------------------
    # SCRAPE SERPER
    #-----------------------------------------------------------
    def scrapeSerper(self, query: str, location: str = "Indonesia", gl: str = "id", hl: str = "id", total_pages: int = 1) -> dict:
        """
        Crawl data menggunakan Serper API (Google Search)
        Dokumentasi: https://serper.dev/

        Args:
            query: Keyword pencarian
            location: Lokasi pencarian (default: Indonesia)
            gl: Country code (default: id)
            hl: Language code (default: id)
            total_pages: Total halaman yang akan di-crawl (default: 1)
                        1 page = 10 hasil, jadi total_pages=10 = 100 hasil

        Returns:
            dict: Hasil crawling dengan list organic results dari semua pages
        """
        import http.client

        logger.info(f"[SERPER] Memulai crawling untuk keyword: {query} ({total_pages} pages)")

        # API Configuration
        API_KEY = "70b6e0bfbc9079ef7860c4c088a777135e1bc68a"
        API_HOST = "google.serper.dev"
        API_PATH = "/search"

        all_organic_results = []

        try:
            # Loop through all pages
            for current_page in range(1, total_pages + 1):
                logger.info(f"[SERPER] Crawling page {current_page}/{total_pages}...")

                # 1. Prepare Request
                conn = http.client.HTTPSConnection(API_HOST)
                payload = json.dumps({
                    "q": query,
                    "location": location,
                    "gl": gl,
                    "hl": hl,
                    "page": current_page  # Current page number
                })
                headers = {
                    'X-API-KEY': API_KEY,
                    'Content-Type': 'application/json'
                }

                # 2. Send Request
                logger.debug(f"[SERPER] Sending request to {API_HOST}{API_PATH} (page {current_page})")
                conn.request("POST", API_PATH, payload, headers)
                res = conn.getresponse()
                data = res.read()

                # 3. Parse Response
                response_data = json.loads(data.decode("utf-8"))
                logger.info(f"[SERPER] Page {current_page} response received, status: {res.status}")

                # 4. Extract Organic Results
                organic_results = response_data.get("organic", [])
                logger.info(f"[SERPER] Page {current_page} found {len(organic_results)} results")

                # Add to combined results
                all_organic_results.extend(organic_results)

                # Close connection
                conn.close()

                # Small delay to avoid rate limiting (optional)
                if current_page < total_pages:
                    import time
                    time.sleep(0.2)  # 200ms delay between requests

            total_results = len(all_organic_results)
            logger.info(f"[SERPER] Total crawled: {total_results} results from {total_pages} pages")

            # 5. Prepare CSV Data
            csv_data = []
            for item in all_organic_results:
                csv_data.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "position": item.get("position", 0),
                    "rating": item.get("rating"),
                    "ratingCount": item.get("ratingCount")
                })

            # 6. Save to CSV
            csv_path = self.saveToCsv(query, csv_data)

            logger.info(f"[SERPER] Data saved to: {csv_path}")

            return {
                "query": query,
                "total_results": total_results,
                "total_pages": total_pages,
                "organic": csv_data,
                "csv_path": csv_path,
                "raw_response": None  # Don't store all raw responses (too large)
            }

        except Exception as e:
            logger.error(f"[SERPER ERROR] Failed to crawl: {e}")
            raise Exception(f"Serper API Error: {str(e)}")

    def saveToCsv(self, keyword: str, data: List[dict]) -> str:
        """
        Save crawling results to CSV file

        Args:
            keyword: Keyword yang dicari (untuk nama file)
            data: List of dict hasil crawling

        Returns:
            str: Path file CSV yang disimpan
        """
        import csv

        # Create directory if not exists
        output_dir = os.path.join(os.getcwd(), "output", "data", "crawl_serper")
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename (sanitize keyword)
        safe_keyword = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_keyword}_{timestamp}.csv"
        csv_path = os.path.join(output_dir, filename)

        # Write to CSV
        if data:
            fieldnames = ["title", "link", "snippet", "position", "rating", "ratingCount"]
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

            logger.info(f"[CSV] Saved {len(data)} rows to {csv_path}")
        else:
            logger.warning(f"[CSV] No data to save for keyword: {keyword}")

        return csv_path


    #-----------------------------------------------------------
    # GET LIST DATASET
    #-----------------------------------------------------------
    def getListDataset(self, is_legal: int, limit_data: int, page: int = 1):
        """
        Get list of dataset from merged CSV based on is_legal filter with pagination

        Args:
            is_legal (int): 1 for legal, 0 for illegal
            limit_data (int): Maximum number of records to return per page
            page (int): Page number (1-indexed)

        Returns:
            dict: Dictionary containing 'data' list and metadata
        """
        import csv
        import os

        # Get project root (3 levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Use merged CSV file
        csv_file = os.path.join(
            project_root,
            'output/data/crawl_serper/ALL_DATA_COMBINED_MERGED.csv'
        )

        logger.info(f"[DATASET] Reading merged CSV from: {csv_file}")

        # Calculate offset for pagination
        offset = (page - 1) * limit_data

        # Read CSV and filter by is_legal
        all_filtered_rows = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Filter by is_legal
                for row in reader:
                    if int(row['is_legal']) == is_legal:
                        all_filtered_rows.append(row)

            total_count = len(all_filtered_rows)

            # Apply pagination
            end_index = offset + limit_data
            paginated_rows = all_filtered_rows[offset:end_index]

            # Convert to result format
            results = []
            for row in paginated_rows:
                results.append({
                    'no': int(row['No']),
                    'keyword': row['Keyword'],
                    'title': row['Title'],
                    'link': row['Link'],
                    'description': row['Description'],
                    'is_legal': int(row['is_legal']),
                    'is_ilegal': int(row['is_ilegal'])
                })

            has_more = end_index < total_count

            logger.info(f"[DATASET] Retrieved {len(results)}/{total_count} records (page={page}, is_legal={is_legal}, limit={limit_data})")

            return {
                'data': results,
                'total_count': total_count,
                'returned_count': len(results),
                'has_more': has_more,
                'current_page': page
            }

        except FileNotFoundError:
            logger.error(f"[DATASET] CSV file not found: {csv_file}")
            raise ValueError(f"Merged dataset file not found")
        except Exception as e:
            logger.error(f"[DATASET] Error reading CSV: {str(e)}")
            raise


    #-----------------------------------------------------------
    # GET DETAIL DATASET
    #-----------------------------------------------------------
    def getDetailDataset(self, id: int):
        """
        Get detail of a single dataset record by ID from merged CSV

        Args:
            id (int): The ID (No) of the dataset record

        Returns:
            dict: Dictionary containing the dataset record

        Raises:
            ValueError: If ID not found
        """
        import csv
        import os

        logger.info(f"[DATASET] Searching for ID={id} in merged CSV")

        # Get project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Use merged CSV file
        csv_file = os.path.join(
            project_root,
            'output/data/crawl_serper/ALL_DATA_COMBINED_MERGED.csv'
        )

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['No']) == id:
                        result = {
                            'id': int(row['No']),
                            'keyword': row['Keyword'],
                            'title': row['Title'],
                            'link': row['Link'],
                            'description': row['Description'],
                            'is_legal': int(row['is_legal']),
                            'is_ilegal': int(row['is_ilegal'])
                        }
                        logger.info(f"[DATASET] Found record with ID={id}")
                        return result

            # If not found
            logger.error(f"[DATASET] Record with ID={id} not found")
            raise ValueError(f"Dataset with ID {id} not found")

        except FileNotFoundError:
            logger.error(f"[DATASET] Merged CSV file not found: {csv_file}")
            raise ValueError(f"Merged dataset file not found")
        except Exception as e:
            logger.error(f"[DATASET] Error reading CSV: {str(e)}")
            raise


    #-----------------------------------------------------------
    # GET DATASET BY LINK
    #-----------------------------------------------------------
    def getDatasetByLink(self, link: str):
        """
        Get single dataset record by link URL

        Args:
            link (str): Link URL to search for

        Returns:
            dict: Single record data

        Raises:
            ValueError: If link not found or file error
        """
        import csv
        import os

        logger.info(f"[DATASET] Searching for link: {link}")

        # Get project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Use merged CSV file
        csv_file = os.path.join(
            project_root,
            'output/data/crawl_serper/ALL_DATA_COMBINED_MERGED.csv'
        )

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Case-insensitive comparison
                    if row['Link'].strip().lower() == link.strip().lower():
                        result = {
                            'id': int(row['No']),
                            'keyword': row['Keyword'],
                            'title': row['Title'],
                            'link': row['Link'],
                            'description': row['Description'],
                            'is_legal': int(row['is_legal']),
                            'is_ilegal': int(row['is_ilegal'])
                        }
                        logger.info(f"[DATASET] Found record with link={link}")
                        return result

            # If not found
            logger.error(f"[DATASET] Record with link={link} not found")
            raise ValueError(f"Dataset with link '{link}' not found")

        except FileNotFoundError:
            logger.error(f"[DATASET] Merged CSV file not found: {csv_file}")
            raise ValueError(f"Merged dataset file not found")
        except Exception as e:
            logger.error(f"[DATASET] Error reading CSV: {str(e)}")
            raise


    #-----------------------------------------------------------
    # SEARCH DATASET
    #-----------------------------------------------------------
    def searchDataset(self, search_query: str, is_legal: int = None, limit_data: int = 10, page: int = 1):
        """
        Search dataset by keyword, title, or description

        Args:
            search_query (str): Search term to find in keyword, title, or description
            is_legal (int): Optional filter by is_legal (1 for legal, 0 for illegal)
            limit_data (int): Maximum number of records to return per page
            page (int): Page number (1-indexed)

        Returns:
            dict: Dictionary containing 'data' list and metadata
        """
        import csv
        import os

        logger.info(f"[DATASET] Searching for '{search_query}' (is_legal={is_legal}, page={page}, limit={limit_data})")

        # Get project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Use merged CSV file
        csv_file = os.path.join(
            project_root,
            'output/data/crawl_serper/ALL_DATA_COMBINED_MERGED.csv'
        )

        # Calculate offset for pagination
        offset = (page - 1) * limit_data

        # Read CSV and search
        all_filtered_rows = []
        search_lower = search_query.lower()

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Filter by is_legal if specified
                    if is_legal is not None and int(row['is_legal']) != is_legal:
                        continue

                    # Search in keyword, title, or description
                    keyword = row.get('Keyword', '').lower()
                    title = row.get('Title', '').lower()
                    description = row.get('Description', '').lower()

                    if search_lower in keyword or search_lower in title or search_lower in description:
                        all_filtered_rows.append(row)

            total_count = len(all_filtered_rows)

            # Apply pagination
            end_index = offset + limit_data
            paginated_rows = all_filtered_rows[offset:end_index]

            # Convert to result format
            results = []
            for row in paginated_rows:
                results.append({
                    'no': int(row['No']),
                    'keyword': row['Keyword'],
                    'title': row['Title'],
                    'link': row['Link'],
                    'description': row['Description'],
                    'is_legal': int(row['is_legal']),
                    'is_ilegal': int(row['is_ilegal'])
                })

            has_more = end_index < total_count

            logger.info(f"[DATASET] Found {total_count} results, returning {len(results)} (page={page})")

            return {
                'data': results,
                'total_count': total_count,
                'returned_count': len(results),
                'has_more': has_more,
                'current_page': page,
                'search_query': search_query
            }

        except FileNotFoundError:
            logger.error(f"[DATASET] CSV file not found: {csv_file}")
            raise ValueError(f"Merged dataset file not found")
        except Exception as e:
            logger.error(f"[DATASET] Error searching CSV: {str(e)}")
            raise
