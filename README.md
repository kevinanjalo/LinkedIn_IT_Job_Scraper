# LinkedIn IT Job Scraper for Sri Lanka

A comprehensive Python-based web scraper designed to collect IT job postings from LinkedIn, specifically focused on the Sri Lankan job market. This project uses a **keyword-by-keyword scraping strategy** to maximize job coverage and is ideal for skill-based job matching and labor market analysis.

##  Project Overview

This scraper implements an intelligent keyword-by-keyword approach to collect IT job data from LinkedIn, enabling:
- **Maximum Coverage**: Searches 100+ IT-related keywords individually
- **Comprehensive Data**: Extracts 500+ technical skills from job descriptions
- **Progressive Saving**: Resilient to failures with incremental data storage
- **Smart Deduplication**: Automatic removal of duplicate jobs across keywords

##  Key Features

### Scraping Strategy
- **Individual Keyword Search**: Each of 100+ keywords searched separately for maximum coverage
- **Complete Pagination**: Scrapes ALL available pages for each keyword (up to 40 pages)
- **Progressive Saving**: Data saved after each keyword (safe from failures)
- **Resumable**: Can stop and restart without losing progress
- **Smart Rate Limiting**: Built-in delays to respect LinkedIn's servers

### Data Collection
- **Core Fields**: Job ID, title, company, location, posted date, job URL
- **Detailed Info**: Description, experience level, employment type, job function, industries
- **Skill Extraction**: 500+ IT skills automatically extracted from descriptions
- **Metadata**: Search keyword, job criteria, number of applicants, scrape timestamp

### IT Focus
- 100+ search keywords covering:
  - Development roles (frontend, backend, fullstack, mobile, web)
  - Specialized technologies (Python, Java, React, Kubernetes, AWS, Azure)
  - Data & Analytics (data scientist, ML engineer, BI analyst)
  - DevOps & Infrastructure (cloud engineer, SRE, platform engineer)
  - Security, QA, UI/UX, Database, and more

##  Use Cases

This dataset is perfect for:
- **ML-Based Job Matching**: Match candidate skills to job requirements
- **Labor Market Analysis**: Understand IT job demand in Sri Lanka
- **Skill Gap Analysis**: Identify in-demand vs. available skills
- **Career Planning**: Discover emerging roles and technologies
- **Resume Optimization**: Align resumes with market demands
- **SDG 8 Research**: Decent work and economic growth analysis

##  Getting Started

### Prerequisites

```python
# Required Python packages
requests
beautifulsoup4
pandas
tqdm
openpyxl
lxml
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kevinanjalo/linkedin-sri-lanka-it-scraper.git
cd linkedin-sri-lanka-it-scraper
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4 pandas tqdm openpyxl lxml
```

3. Open the Jupyter Notebook:
```bash
jupyter notebook LinkedIn_IT_Job_Scraper_(Sri_Lanka).ipynb
```

### Usage

1. **Configure Settings** (Step 2):
   - Modify `CONFIG` dictionary to adjust delays and pagination limits
   - Default: Scrapes up to 40 pages per keyword

2. **Run Scraping** (Steps 3-7):
   - Execute cells sequentially
   - Monitor progress in real-time
   - Data saved progressively after each keyword

3. **Generate Reports** (Steps 8-9):
   - Final deduplication and CSV generation
   - Excel file with formatted data
   - Comprehensive summary statistics

##  Output Files

The scraper generates three files in the `data/` directory:

1. **CSV File**: `linkedin_sri_lanka_IT_jobs_final.csv`
   - Deduplicated dataset with all job records
   - Ready for ML processing

2. **Excel File**: `linkedin_sri_lanka_IT_jobs_{timestamp}.xlsx`
   - Formatted spreadsheet for manual analysis
   - Multiple sheets with statistics

3. **Summary Report**: `scraping_summary_{timestamp}.txt`
   - Keyword effectiveness statistics
   - Top companies and job titles
   - Data completeness metrics
   - Most in-demand skills

## 🔍 Data Fields

| Field | Description |
|-------|-------------|
| `job_id` | Unique LinkedIn job identifier |
| `title` | Job title |
| `company` | Company name |
| `location` | Job location |
| `posted_date` | Date job was posted |
| `description` | Full job description text |
| `required_skills` | Extracted IT skills (comma-separated) |
| `experience_level` | Entry, Mid-Senior, Executive, etc. |
| `employment_type` | Full-time, Contract, Part-time, etc. |
| `job_function` | Engineering, IT, Product Management, etc. |
| `industries` | Company industries |
| `num_applicants` | Number of applicants |
| `search_keyword` | Keyword that found this job |
| `job_url` | Direct link to job posting |
| `scraped_at` | Timestamp of data collection |

## 🎓 Search Keywords (100+)

The scraper uses comprehensive IT keywords across multiple categories:

### Development Roles
- Software developer, engineer, programmer
- Frontend, backend, fullstack developer
- Mobile, web, application developer

### Technologies
- Python, Java, JavaScript, .NET, PHP, Ruby, Go
- React, Angular, Vue, Node.js
- iOS, Android, Flutter, React Native

### Specialized Roles
- DevOps engineer, cloud engineer, SRE
- Data scientist, data engineer, ML engineer
- QA engineer, security engineer, DBA

### Emerging Tech
- AI/ML, blockchain, IoT, Web3
- Cloud (AWS, Azure, GCP)
- Kubernetes, Docker, CI/CD

##  Why Keyword-by-Keyword?

| Aspect | Traditional Approach | Keyword-by-Keyword |
|--------|---------------------|-------------------|
| **Coverage** | Combined OR keywords | Each keyword separately |
| **Pagination** | Limited by filters | ALL pages per keyword |
| **Resilience** | Lose all if fails | Progressive save |
| **Resumable** | No | Yes |
| **Deduplication** | Per filter combo | Across all keywords |
| **Max Jobs** | ~4,000 | 100,000+ potential |

##  Configuration Options

```python
CONFIG = {
    'location': 'Sri Lanka',
    'output_dir': 'data',
    'request_delay': (2, 4),      # Delay between requests (seconds)
    'page_delay': (3, 6),          # Delay between pages (seconds)
    'keyword_delay': (10, 15),     # Delay between keywords (seconds)
    'max_pages_per_keyword': 40,   # Max pages to scrape per keyword
}
```

##  Ethical Considerations

- **Educational Use**: This scraper is designed for academic research and educational purposes only
- **Rate Limiting**: Built-in delays respect LinkedIn's servers
- **No Authentication**: Uses only public job listings
- **Robots.txt**: Compliant with LinkedIn's terms of service for educational scraping
- **Data Privacy**: No personal information collected

##  SDG Alignment

This project supports **SDG 8: Decent Work and Economic Growth** by:
- Providing comprehensive job market insights
- Enabling better job-skill matching
- Supporting workforce development initiatives
- Identifying skill gaps in the labor market

##  Sample Statistics

After scraping, you'll get insights like:
- Total unique IT jobs in Sri Lanka
- Top hiring companies
- Most in-demand skills
- Popular job titles and roles
- Experience level distribution
- Employment type breakdown

##  Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Add new search keywords
- Enhance skill extraction

##  License

This project is open source and available for educational purposes. Please ensure compliance with LinkedIn's terms of service and use responsibly.

##  Author

**Kevin Anjalo**
- GitHub: [@kevinanjalo](https://github.com/kevinanjalo)

##  Acknowledgments

- Built for skill-aware job matching research
- Supports labor market analysis in Sri Lanka
- Contributes to SDG 8 objectives

##  Disclaimer

This scraper is provided for **educational and research purposes only**. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Respecting rate limits and server resources
- Using data ethically and responsibly
- Following local data protection regulations

---

**Note**: Estimated scraping time is 2-4 hours for all 100+ keywords with built-in delays. The scraper is fully resumable and saves progress incrementally.
