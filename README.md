# LinkedIn IT Job Scraper

A comprehensive LinkedIn job scraper that systematically searches over 100 keywords individually—covering roles (developer, architect), specializations (devops, fullstack), and technologies (python, AWS)—and scrapes all available pages for each search term. This ensures maximum coverage of the entire IT job market.

## Features

- **100+ Keywords**: Comprehensive coverage of IT job market including:
  - **Roles**: developer, architect, engineer, tech lead, etc.
  - **Specializations**: devops, fullstack, data engineer, machine learning, etc.
  - **Technologies**: python, AWS, kubernetes, docker, react, etc.
  
- **Complete Page Scraping**: Automatically scrapes all available pages for each keyword

- **Data Export**: Results saved in both JSON and CSV formats

- **Statistics**: Detailed statistics on jobs found per keyword

- **Respectful Scraping**: Built-in delays to respect server resources

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kevinanjalo/LinkedIn_IT_Job_Scraper.git
cd LinkedIn_IT_Job_Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Test Mode)

Run the scraper in test mode with a limited number of keywords:

```bash
python scraper.py
```

This will scrape the first 5 keywords with up to 3 pages each.

### Full Scraping Mode

To scrape all 100+ keywords, edit `scraper.py` and uncomment line 318:

```python
def main():
    logger.info("LinkedIn IT Job Scraper Starting...")
    logger.info(f"Total keywords available: {get_keyword_count()}")
    
    scraper = LinkedInJobScraper(output_dir="output", delay=2.0)
    
    # Uncomment the line below for full scraping
    scraper.scrape_all_keywords()
    
    # Comment out or remove the test mode section
    # test_keywords = get_all_keywords()[:5]
    # scraper.scrape_all_keywords(keywords=test_keywords, max_pages_per_keyword=3)
```

### Custom Keywords

You can also scrape specific keywords:

```python
from scraper import LinkedInJobScraper

scraper = LinkedInJobScraper()
custom_keywords = ["python developer", "aws engineer", "devops"]
scraper.scrape_all_keywords(keywords=custom_keywords, max_pages_per_keyword=10)
```

## Output

The scraper creates an `output/` directory with:

1. **JSON file**: `final_jobs_YYYYMMDD_HHMMSS.json`
   - Complete job data in JSON format
   
2. **CSV file**: `final_jobs_YYYYMMDD_HHMMSS.csv`
   - Job data in CSV format for easy analysis in Excel/spreadsheets
   
3. **Statistics file**: `final_stats_YYYYMMDD_HHMMSS.txt`
   - Summary statistics including:
     - Total keywords processed
     - Total jobs found
     - Jobs per keyword breakdown

4. **Log file**: `scraper.log`
   - Detailed logging of the scraping process

### Example Output Structure

Each job entry contains:
```json
{
  "keyword": "python developer",
  "title": "Senior Python Developer",
  "company": "Tech Company Inc.",
  "location": "San Francisco, CA",
  "job_url": "https://www.linkedin.com/jobs/view/...",
  "posted_date": "2024-01-15",
  "scraped_at": "2024-01-20T10:30:00"
}
```

## Keyword Categories

The scraper includes keywords from the following categories:

### Roles (20 keywords)
developer, software engineer, architect, tech lead, engineering manager, CTO, etc.

### Specializations (30 keywords)
devops, fullstack, data engineer, machine learning engineer, cloud engineer, security engineer, etc.

### Programming Languages (19 keywords)
python, java, javascript, typescript, go, rust, etc.

### Cloud & Infrastructure (13 keywords)
AWS, Azure, GCP, kubernetes, docker, terraform, etc.

### Frameworks & Libraries (20 keywords)
react, angular, django, spring, nodejs, tensorflow, etc.

### Databases (13 keywords)
SQL, PostgreSQL, MongoDB, Redis, Elasticsearch, etc.

### Other Technologies (12 keywords)
REST API, GraphQL, microservices, agile, CI/CD, etc.

**Total: 127 unique keywords**

## Configuration

You can customize the scraper behavior in `scraper.py`:

- `output_dir`: Directory to save results (default: "output")
- `delay`: Delay between requests in seconds (default: 2.0)
- `max_pages_per_keyword`: Maximum pages to scrape per keyword (default: 40)

## Important Notes

⚠️ **Legal & Ethical Considerations**:
- This scraper is for educational and research purposes
- Respect LinkedIn's Terms of Service and robots.txt
- Use reasonable delays between requests
- Consider using LinkedIn's official API for production use
- Be aware that web scraping may be restricted by LinkedIn's policies

⚠️ **Technical Considerations**:
- LinkedIn's HTML structure may change, requiring updates to selectors
- Rate limiting may occur with aggressive scraping
- Authentication may be required for full access to job listings
- Some job listings may require login to view full details

## Troubleshooting

**No jobs found**: LinkedIn's HTML structure may have changed. Check the `extract_job_info` method and update CSS selectors.

**Connection errors**: Reduce scraping speed by increasing the `delay` parameter.

**Empty results**: LinkedIn may be blocking automated requests. Consider adding authentication or using proxies.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is provided for educational purposes only. Users are responsible for ensuring their use complies with LinkedIn's Terms of Service and applicable laws.