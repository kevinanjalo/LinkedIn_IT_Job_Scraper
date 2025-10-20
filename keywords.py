"""
Comprehensive keyword list for LinkedIn IT job scraping.
Contains 100+ keywords covering roles, specializations, and technologies.
"""

# Job Roles
ROLES = [
    "developer",
    "software engineer",
    "programmer",
    "architect",
    "tech lead",
    "engineering manager",
    "cto",
    "vp engineering",
    "principal engineer",
    "staff engineer",
    "senior engineer",
    "junior developer",
    "frontend developer",
    "backend developer",
    "web developer",
    "mobile developer",
    "game developer",
    "software developer",
    "application developer",
    "systems engineer",
]

# Specializations
SPECIALIZATIONS = [
    "devops",
    "fullstack",
    "full stack",
    "data engineer",
    "data scientist",
    "machine learning engineer",
    "ml engineer",
    "ai engineer",
    "artificial intelligence",
    "cloud engineer",
    "security engineer",
    "qa engineer",
    "test engineer",
    "automation engineer",
    "site reliability engineer",
    "sre",
    "platform engineer",
    "infrastructure engineer",
    "network engineer",
    "database administrator",
    "dba",
    "system administrator",
    "sysadmin",
    "blockchain developer",
    "embedded systems",
    "iot developer",
    "big data engineer",
    "etl developer",
    "analytics engineer",
    "business intelligence",
]

# Programming Languages
PROGRAMMING_LANGUAGES = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "go",
    "golang",
    "rust",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "scala",
    "r",
    "perl",
    "shell",
    "bash",
    "powershell",
]

# Cloud & Infrastructure
CLOUD_TECHNOLOGIES = [
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "kubernetes",
    "k8s",
    "docker",
    "terraform",
    "ansible",
    "jenkins",
    "gitlab",
    "circleci",
    "cloudformation",
]

# Frameworks & Libraries
FRAMEWORKS = [
    "react",
    "angular",
    "vue",
    "django",
    "flask",
    "spring",
    "springboot",
    "nodejs",
    "node.js",
    "express",
    "fastapi",
    "laravel",
    "rails",
    "asp.net",
    ".net core",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
]

# Databases
DATABASES = [
    "sql",
    "nosql",
    "postgresql",
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "cassandra",
    "dynamodb",
    "oracle",
    "sql server",
    "mariadb",
]

# Other Technologies
OTHER_TECHNOLOGIES = [
    "rest api",
    "graphql",
    "microservices",
    "agile",
    "scrum",
    "ci/cd",
    "git",
    "linux",
    "windows",
    "api",
    "blockchain",
    "cybersecurity",
]

def get_all_keywords():
    """
    Combine all keyword categories into a single comprehensive list.
    Returns a deduplicated list of all keywords.
    """
    all_keywords = (
        ROLES +
        SPECIALIZATIONS +
        PROGRAMMING_LANGUAGES +
        CLOUD_TECHNOLOGIES +
        FRAMEWORKS +
        DATABASES +
        OTHER_TECHNOLOGIES
    )
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in all_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower not in seen:
            seen.add(keyword_lower)
            unique_keywords.append(keyword)
    
    return unique_keywords

def get_keyword_count():
    """Return the total number of unique keywords."""
    return len(get_all_keywords())
