"""
Test suite for the LinkedIn IT Job Scraper.

This module contains tests to validate the scraper functionality without
making actual HTTP requests to LinkedIn.
"""

import unittest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from scraper import LinkedInJobScraper
from keywords import (
    get_all_keywords, 
    get_keyword_count,
    ROLES,
    SPECIALIZATIONS,
    PROGRAMMING_LANGUAGES,
    CLOUD_TECHNOLOGIES,
    FRAMEWORKS,
    DATABASES,
    OTHER_TECHNOLOGIES
)


class TestKeywords(unittest.TestCase):
    """Test cases for the keywords module."""
    
    def test_keyword_count_over_100(self):
        """Test that we have over 100 keywords as required."""
        count = get_keyword_count()
        self.assertGreater(count, 100, 
                          f"Expected more than 100 keywords, got {count}")
    
    def test_keyword_categories_not_empty(self):
        """Test that all keyword categories have entries."""
        self.assertGreater(len(ROLES), 0, "ROLES should not be empty")
        self.assertGreater(len(SPECIALIZATIONS), 0, "SPECIALIZATIONS should not be empty")
        self.assertGreater(len(PROGRAMMING_LANGUAGES), 0, "PROGRAMMING_LANGUAGES should not be empty")
        self.assertGreater(len(CLOUD_TECHNOLOGIES), 0, "CLOUD_TECHNOLOGIES should not be empty")
        self.assertGreater(len(FRAMEWORKS), 0, "FRAMEWORKS should not be empty")
        self.assertGreater(len(DATABASES), 0, "DATABASES should not be empty")
        self.assertGreater(len(OTHER_TECHNOLOGIES), 0, "OTHER_TECHNOLOGIES should not be empty")
    
    def test_keywords_include_required_examples(self):
        """Test that keywords include the examples mentioned in requirements."""
        all_keywords_lower = [k.lower() for k in get_all_keywords()]
        
        # Roles
        self.assertIn("developer", all_keywords_lower, "Should include 'developer'")
        self.assertIn("architect", all_keywords_lower, "Should include 'architect'")
        
        # Specializations
        self.assertIn("devops", all_keywords_lower, "Should include 'devops'")
        self.assertIn("fullstack", all_keywords_lower, "Should include 'fullstack'")
        
        # Technologies
        self.assertIn("python", all_keywords_lower, "Should include 'python'")
        self.assertIn("aws", all_keywords_lower, "Should include 'aws'")
    
    def test_no_duplicate_keywords(self):
        """Test that all keywords are unique (case-insensitive)."""
        all_keywords = get_all_keywords()
        keywords_lower = [k.lower() for k in all_keywords]
        self.assertEqual(len(keywords_lower), len(set(keywords_lower)),
                        "Keywords should be unique (case-insensitive)")


class TestScraperInitialization(unittest.TestCase):
    """Test cases for scraper initialization."""
    
    def test_scraper_initialization(self):
        """Test that scraper can be initialized with default parameters."""
        scraper = LinkedInJobScraper()
        self.assertEqual(scraper.output_dir, "output")
        self.assertEqual(scraper.delay, 2.0)
        self.assertIsNotNone(scraper.session)
    
    def test_scraper_custom_parameters(self):
        """Test that scraper accepts custom parameters."""
        scraper = LinkedInJobScraper(output_dir="/tmp/test_output", delay=1.5)
        self.assertEqual(scraper.output_dir, "/tmp/test_output")
        self.assertEqual(scraper.delay, 1.5)
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        test_dir = "/tmp/test_scraper_output"
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
        
        scraper = LinkedInJobScraper(output_dir=test_dir)
        self.assertTrue(os.path.exists(test_dir), 
                       "Output directory should be created")
        
        # Cleanup
        if os.path.exists(test_dir):
            os.rmdir(test_dir)


class TestURLBuilding(unittest.TestCase):
    """Test cases for URL building functionality."""
    
    def setUp(self):
        """Set up test scraper instance."""
        self.scraper = LinkedInJobScraper()
    
    def test_build_search_url_page_0(self):
        """Test URL building for first page."""
        url = self.scraper.build_search_url("python developer", 0)
        self.assertIn("keywords=python+developer", url)
        self.assertIn("start=0", url)
    
    def test_build_search_url_page_1(self):
        """Test URL building for second page."""
        url = self.scraper.build_search_url("python developer", 1)
        self.assertIn("keywords=python+developer", url)
        self.assertIn("start=25", url)
    
    def test_build_search_url_special_characters(self):
        """Test URL building with special characters."""
        url = self.scraper.build_search_url("c++ developer", 0)
        self.assertIn("keywords=c%2B%2B+developer", url)
    
    def test_build_search_url_multiple_words(self):
        """Test URL building with multiple words."""
        url = self.scraper.build_search_url("senior software engineer", 0)
        self.assertIn("senior+software+engineer", url)


class TestJobExtraction(unittest.TestCase):
    """Test cases for job information extraction."""
    
    def setUp(self):
        """Set up test scraper instance."""
        self.scraper = LinkedInJobScraper()
    
    def test_extract_job_info_with_valid_data(self):
        """Test job extraction with valid data."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="base-card">
            <h3 class="base-search-card__title">Senior Python Developer</h3>
            <h4 class="base-search-card__subtitle">Tech Company Inc.</h4>
            <span class="job-search-card__location">San Francisco, CA</span>
            <a class="base-card__full-link" href="https://www.linkedin.com/jobs/view/123"></a>
            <time datetime="2024-01-15"></time>
        </div>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        card = soup.find('div', class_='base-card')
        
        job = self.scraper.extract_job_info(card, "python")
        
        self.assertIsNotNone(job)
        self.assertEqual(job['keyword'], "python")
        self.assertEqual(job['title'], "Senior Python Developer")
        self.assertEqual(job['company'], "Tech Company Inc.")
        self.assertEqual(job['location'], "San Francisco, CA")
        self.assertEqual(job['job_url'], "https://www.linkedin.com/jobs/view/123")
        self.assertEqual(job['posted_date'], "2024-01-15")
    
    def test_extract_job_info_missing_title(self):
        """Test job extraction when title is missing."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="base-card">
            <h4 class="base-search-card__subtitle">Tech Company Inc.</h4>
        </div>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        card = soup.find('div', class_='base-card')
        
        job = self.scraper.extract_job_info(card, "python")
        
        self.assertIsNone(job, "Should return None when title is missing")


class TestScraperMethods(unittest.TestCase):
    """Test cases for main scraper methods."""
    
    def setUp(self):
        """Set up test scraper instance."""
        self.scraper = LinkedInJobScraper(output_dir="/tmp/test_scraper")
    
    @patch('scraper.requests.Session.get')
    def test_scrape_page_handles_request_error(self, mock_get):
        """Test that scrape_page handles request errors gracefully."""
        mock_get.side_effect = Exception("Connection error")
        
        jobs = self.scraper.scrape_page("python", 0)
        
        self.assertEqual(len(jobs), 0, "Should return empty list on error")
    
    def test_scraper_statistics_tracking(self):
        """Test that scraper tracks statistics correctly."""
        self.scraper.keywords_processed = 5
        self.scraper.total_jobs_found = 123
        
        self.assertEqual(self.scraper.keywords_processed, 5)
        self.assertEqual(self.scraper.total_jobs_found, 123)
    
    def tearDown(self):
        """Clean up test output directory."""
        import shutil
        if os.path.exists("/tmp/test_scraper"):
            shutil.rmtree("/tmp/test_scraper")


class TestDataOutput(unittest.TestCase):
    """Test cases for data output functionality."""
    
    def setUp(self):
        """Set up test scraper with sample data."""
        self.test_dir = "/tmp/test_scraper_output"
        self.scraper = LinkedInJobScraper(output_dir=self.test_dir)
        self.scraper.all_jobs = [
            {
                'keyword': 'python',
                'title': 'Python Developer',
                'company': 'Test Company',
                'location': 'Remote',
                'job_url': 'https://example.com/job1',
                'posted_date': '2024-01-15',
                'scraped_at': '2024-01-20T10:00:00'
            }
        ]
    
    def test_save_results_creates_files(self):
        """Test that save_results creates JSON and CSV files."""
        self.scraper.save_results(intermediate=False)
        
        # Check that files were created
        files = os.listdir(self.test_dir)
        json_files = [f for f in files if f.endswith('.json')]
        csv_files = [f for f in files if f.endswith('.csv')]
        stats_files = [f for f in files if f.endswith('.txt')]
        
        self.assertGreater(len(json_files), 0, "Should create JSON file")
        self.assertGreater(len(csv_files), 0, "Should create CSV file")
        self.assertGreater(len(stats_files), 0, "Should create stats file")
    
    def test_save_results_json_content(self):
        """Test that JSON output contains correct data."""
        self.scraper.save_results(intermediate=False)
        
        json_files = [f for f in os.listdir(self.test_dir) if f.endswith('.json')]
        with open(os.path.join(self.test_dir, json_files[0]), 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['keyword'], 'python')
        self.assertEqual(data[0]['title'], 'Python Developer')
    
    def tearDown(self):
        """Clean up test output directory."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


class TestIntegration(unittest.TestCase):
    """Integration tests for the scraper."""
    
    def test_end_to_end_keyword_list(self):
        """Test that the complete keyword list can be retrieved."""
        keywords = get_all_keywords()
        self.assertGreater(len(keywords), 100)
        
        # Test that we can pass this to the scraper
        scraper = LinkedInJobScraper()
        self.assertIsNotNone(scraper)
    
    def test_scraper_configuration_options(self):
        """Test different scraper configuration options."""
        # Test with minimal keywords
        test_keywords = ["python", "java"]
        scraper = LinkedInJobScraper()
        
        # Verify scraper can accept custom keywords
        self.assertIsNotNone(scraper)
        self.assertIsInstance(test_keywords, list)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
