"""
Example configuration and usage patterns for the LinkedIn IT Job Scraper.
"""

from scraper import LinkedInJobScraper
from keywords import get_all_keywords, ROLES, SPECIALIZATIONS, PROGRAMMING_LANGUAGES

# Example 1: Full scraping with all keywords
def full_scrape():
    """Scrape all 100+ keywords with maximum coverage."""
    scraper = LinkedInJobScraper(output_dir="output", delay=2.0)
    scraper.scrape_all_keywords(max_pages_per_keyword=40)

# Example 2: Focus on specific roles only
def scrape_roles_only():
    """Scrape only job role keywords."""
    scraper = LinkedInJobScraper(output_dir="output/roles", delay=2.0)
    scraper.scrape_all_keywords(keywords=ROLES, max_pages_per_keyword=30)

# Example 3: Focus on programming languages
def scrape_languages():
    """Scrape only programming language keywords."""
    scraper = LinkedInJobScraper(output_dir="output/languages", delay=2.0)
    scraper.scrape_all_keywords(keywords=PROGRAMMING_LANGUAGES, max_pages_per_keyword=20)

# Example 4: Custom keyword list
def scrape_custom_keywords():
    """Scrape a custom list of high-priority keywords."""
    custom_keywords = [
        "python developer",
        "java developer", 
        "devops engineer",
        "cloud architect",
        "aws",
        "kubernetes",
        "react developer",
        "fullstack developer"
    ]
    scraper = LinkedInJobScraper(output_dir="output/custom", delay=1.5)
    scraper.scrape_all_keywords(keywords=custom_keywords, max_pages_per_keyword=25)

# Example 5: Quick test with minimal keywords
def quick_test():
    """Quick test with a few keywords and pages."""
    test_keywords = ["python", "javascript", "devops"]
    scraper = LinkedInJobScraper(output_dir="output/test", delay=1.0)
    scraper.scrape_all_keywords(keywords=test_keywords, max_pages_per_keyword=2)

# Example 6: Scrape with faster delays (be careful with rate limiting)
def fast_scrape():
    """Scrape with minimal delays (use cautiously)."""
    scraper = LinkedInJobScraper(output_dir="output", delay=0.5)
    keywords = get_all_keywords()[:10]  # First 10 keywords
    scraper.scrape_all_keywords(keywords=keywords, max_pages_per_keyword=15)

# Example 7: Conservative scraping with longer delays
def conservative_scrape():
    """Scrape with longer delays to minimize detection risk."""
    scraper = LinkedInJobScraper(output_dir="output", delay=5.0)
    scraper.scrape_all_keywords(max_pages_per_keyword=30)


if __name__ == "__main__":
    # Choose one of the examples above
    print("LinkedIn IT Job Scraper - Example Configurations")
    print("\nAvailable examples:")
    print("1. full_scrape() - Scrape all 100+ keywords")
    print("2. scrape_roles_only() - Scrape only job roles")
    print("3. scrape_languages() - Scrape only programming languages")
    print("4. scrape_custom_keywords() - Scrape custom keyword list")
    print("5. quick_test() - Quick test with 3 keywords")
    print("6. fast_scrape() - Fast scraping (use cautiously)")
    print("7. conservative_scrape() - Conservative with long delays")
    print("\nEdit this file and uncomment the desired example.")
    
    # Uncomment one of these to run:
    # full_scrape()
    # scrape_roles_only()
    # scrape_languages()
    # scrape_custom_keywords()
    quick_test()  # Running quick test by default
    # fast_scrape()
    # conservative_scrape()
