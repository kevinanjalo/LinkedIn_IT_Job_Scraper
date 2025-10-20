"""
LinkedIn IT Job Scraper

This scraper systematically searches over 100 keywords individually—covering 
roles (developer, architect), specializations (devops, fullstack), and 
technologies (python, AWS)—and scrapes all available pages for each search term.
This ensures maximum coverage of the entire IT job market.
"""

import time
import csv
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import os

import requests
from bs4 import BeautifulSoup

from keywords import get_all_keywords, get_keyword_count


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LinkedInJobScraper:
    """
    LinkedIn IT Job Scraper that searches multiple keywords and scrapes all pages.
    """
    
    BASE_URL = "https://www.linkedin.com/jobs/search/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    def __init__(self, output_dir: str = "output", delay: float = 2.0):
        """
        Initialize the scraper.
        
        Args:
            output_dir: Directory to save scraped data
            delay: Delay between requests in seconds (default: 2.0)
        """
        self.output_dir = output_dir
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        self.all_jobs = []
        self.keywords_processed = 0
        self.total_jobs_found = 0
        
    def build_search_url(self, keyword: str, page: int = 0) -> str:
        """
        Build LinkedIn job search URL for a given keyword and page.
        
        Args:
            keyword: Search keyword
            page: Page number (LinkedIn uses 'start' parameter, 0-indexed by 25)
            
        Returns:
            Complete search URL
        """
        encoded_keyword = quote_plus(keyword)
        start = page * 25  # LinkedIn shows 25 jobs per page
        url = f"{self.BASE_URL}?keywords={encoded_keyword}&start={start}"
        return url
    
    def scrape_page(self, keyword: str, page: int) -> List[Dict]:
        """
        Scrape a single page of job listings for a keyword.
        
        Args:
            keyword: Search keyword
            page: Page number
            
        Returns:
            List of job dictionaries
        """
        url = self.build_search_url(keyword, page)
        jobs = []
        
        try:
            logger.info(f"Scraping {keyword} - Page {page + 1}: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards (LinkedIn's structure may vary)
            # This is a simplified example - actual LinkedIn structure may differ
            job_cards = soup.find_all('div', class_='base-card')
            
            if not job_cards:
                # Try alternative selectors
                job_cards = soup.find_all('li', class_='job-search-card')
            
            for card in job_cards:
                job = self.extract_job_info(card, keyword)
                if job:
                    jobs.append(job)
            
            logger.info(f"Found {len(jobs)} jobs on page {page + 1} for keyword: {keyword}")
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {keyword} page {page + 1}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error scraping {keyword} page {page + 1}: {str(e)}")
        
        return jobs
    
    def extract_job_info(self, card, keyword: str) -> Optional[Dict]:
        """
        Extract job information from a job card element.
        
        Args:
            card: BeautifulSoup element containing job card
            keyword: Search keyword used to find this job
            
        Returns:
            Dictionary containing job information
        """
        try:
            job_data = {
                'keyword': keyword,
                'title': '',
                'company': '',
                'location': '',
                'job_url': '',
                'posted_date': '',
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract title
            title_elem = card.find('h3', class_='base-search-card__title')
            if not title_elem:
                title_elem = card.find('h3')
            if title_elem:
                job_data['title'] = title_elem.get_text(strip=True)
            
            # Extract company
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            if not company_elem:
                company_elem = card.find('a', class_='hidden-nested-link')
            if company_elem:
                job_data['company'] = company_elem.get_text(strip=True)
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            if location_elem:
                job_data['location'] = location_elem.get_text(strip=True)
            
            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            if not link_elem:
                link_elem = card.find('a')
            if link_elem and link_elem.get('href'):
                job_data['job_url'] = link_elem['href']
            
            # Extract posted date
            time_elem = card.find('time')
            if time_elem:
                job_data['posted_date'] = time_elem.get('datetime', '')
            
            # Only return if we have at least a title
            if job_data['title']:
                return job_data
                
        except Exception as e:
            logger.error(f"Error extracting job info: {str(e)}")
        
        return None
    
    def scrape_keyword(self, keyword: str, max_pages: int = 40) -> List[Dict]:
        """
        Scrape all available pages for a specific keyword.
        
        Args:
            keyword: Search keyword
            max_pages: Maximum number of pages to scrape (default: 40, which is ~1000 jobs)
            
        Returns:
            List of all jobs found for this keyword
        """
        logger.info(f"Starting to scrape keyword: '{keyword}'")
        all_jobs_for_keyword = []
        consecutive_empty_pages = 0
        max_consecutive_empty = 3  # Stop if we get 3 consecutive empty pages
        
        for page in range(max_pages):
            jobs = self.scrape_page(keyword, page)
            
            if jobs:
                all_jobs_for_keyword.extend(jobs)
                consecutive_empty_pages = 0
            else:
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= max_consecutive_empty:
                    logger.info(f"No jobs found for {consecutive_empty_pages} consecutive pages. Stopping pagination for keyword: {keyword}")
                    break
            
            # Be respectful with delays
            time.sleep(self.delay)
        
        logger.info(f"Completed scraping keyword '{keyword}': Found {len(all_jobs_for_keyword)} jobs across {page + 1} pages")
        return all_jobs_for_keyword
    
    def scrape_all_keywords(self, keywords: Optional[List[str]] = None, max_pages_per_keyword: int = 40):
        """
        Scrape all keywords systematically.
        
        Args:
            keywords: List of keywords to scrape (defaults to all predefined keywords)
            max_pages_per_keyword: Maximum pages to scrape per keyword
        """
        if keywords is None:
            keywords = get_all_keywords()
        
        total_keywords = len(keywords)
        logger.info(f"Starting comprehensive scrape of {total_keywords} keywords")
        logger.info(f"Keywords: {', '.join(keywords[:10])}... (showing first 10)")
        
        start_time = time.time()
        
        for idx, keyword in enumerate(keywords, 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"Progress: {idx}/{total_keywords} ({(idx/total_keywords)*100:.1f}%)")
            logger.info(f"Keyword: '{keyword}'")
            logger.info(f"{'='*80}\n")
            
            jobs = self.scrape_keyword(keyword, max_pages=max_pages_per_keyword)
            self.all_jobs.extend(jobs)
            self.keywords_processed += 1
            self.total_jobs_found += len(jobs)
            
            # Save intermediate results every 10 keywords
            if idx % 10 == 0:
                self.save_results(intermediate=True)
        
        elapsed_time = time.time() - start_time
        logger.info(f"\n{'='*80}")
        logger.info(f"SCRAPING COMPLETED!")
        logger.info(f"Total Keywords Processed: {self.keywords_processed}")
        logger.info(f"Total Jobs Found: {self.total_jobs_found}")
        logger.info(f"Time Elapsed: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        logger.info(f"{'='*80}\n")
        
        # Save final results
        self.save_results(intermediate=False)
    
    def save_results(self, intermediate: bool = False):
        """
        Save scraped results to files.
        
        Args:
            intermediate: Whether this is an intermediate save
        """
        if not self.all_jobs:
            logger.warning("No jobs to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = "intermediate_" if intermediate else "final_"
        
        # Save as JSON
        json_filename = os.path.join(self.output_dir, f"{prefix}jobs_{timestamp}.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_jobs, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(self.all_jobs)} jobs to {json_filename}")
        
        # Save as CSV
        csv_filename = os.path.join(self.output_dir, f"{prefix}jobs_{timestamp}.csv")
        if self.all_jobs:
            keys = self.all_jobs[0].keys()
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.all_jobs)
            logger.info(f"Saved {len(self.all_jobs)} jobs to {csv_filename}")
        
        # Save summary statistics
        stats_filename = os.path.join(self.output_dir, f"{prefix}stats_{timestamp}.txt")
        with open(stats_filename, 'w', encoding='utf-8') as f:
            f.write(f"LinkedIn IT Job Scraper - Statistics\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Keywords Processed: {self.keywords_processed}\n")
            f.write(f"Total Jobs Found: {self.total_jobs_found}\n")
            f.write(f"Unique Jobs: {len(self.all_jobs)}\n")
            
            # Count jobs by keyword
            keyword_counts = {}
            for job in self.all_jobs:
                keyword = job.get('keyword', 'unknown')
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            
            f.write(f"\nJobs per Keyword:\n")
            for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {keyword}: {count}\n")
        
        logger.info(f"Saved statistics to {stats_filename}")


def main():
    """Main entry point for the scraper."""
    logger.info("LinkedIn IT Job Scraper Starting...")
    logger.info(f"Total keywords available: {get_keyword_count()}")
    
    # Initialize scraper
    scraper = LinkedInJobScraper(output_dir="output", delay=2.0)
    
    # Option 1: Scrape all keywords (100+)
    # scraper.scrape_all_keywords()
    
    # Option 2: Scrape a subset of keywords for testing
    test_keywords = get_all_keywords()[:5]  # First 5 keywords for testing
    logger.info(f"Running in TEST MODE with {len(test_keywords)} keywords: {test_keywords}")
    scraper.scrape_all_keywords(keywords=test_keywords, max_pages_per_keyword=3)
    
    logger.info("Scraping completed!")


if __name__ == "__main__":
    main()
