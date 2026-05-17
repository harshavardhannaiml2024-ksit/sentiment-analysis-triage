# Project Manifest

**Project:** Sentiment Analysis Triage System  
**Version:** 1.0.0  
**Last Updated:** 2026-05-17  
**Export Date:** Generated with export scripts

---

## 📋 Table of Contents

- [Core Application Files](#core-application-files)
- [Configuration Files](#configuration-files)
- [Source Code Modules](#source-code-modules)
- [Data Connectors](#data-connectors)
- [Utility Modules](#utility-modules)
- [Documentation](#documentation)
- [Deployment Files](#deployment-files)
- [Data Files](#data-files)
- [GitHub Workflows](#github-workflows)
- [Export Scripts](#export-scripts)

---

## 🎯 Core Application Files

### `app.py`
**Type:** Python Application  
**Purpose:** Main Streamlit application entry point  
**Description:** Orchestrates the entire sentiment analysis and triage system. Provides the web interface for uploading feedback data, analyzing sentiment, calculating priority scores, and visualizing results. Integrates all modules and connectors.

### `requirements.txt`
**Type:** Python Dependencies  
**Purpose:** Package dependency specification  
**Description:** Lists all Python packages required to run the application, including Streamlit, transformers, pandas, plotly, and database connectors.

---

## ⚙️ Configuration Files

### `config.yaml`
**Type:** YAML Configuration  
**Purpose:** Application configuration  
**Description:** Central configuration file containing settings for sentiment analysis models, priority scoring weights, data source configurations, and application behavior parameters.

### `.env.example`
**Type:** Environment Template  
**Purpose:** Environment variables template  
**Description:** Example file showing required environment variables for database connections, API keys, and sensitive configuration. Users copy this to `.env` and fill in actual values.

### `.gitignore`
**Type:** Git Configuration  
**Purpose:** Version control exclusions  
**Description:** Specifies files and directories that should not be tracked by Git, including virtual environments, cache files, secrets, and build artifacts.

### `.dockerignore`
**Type:** Docker Configuration  
**Purpose:** Docker build exclusions  
**Description:** Lists files and directories to exclude from Docker build context, reducing image size and build time.

---

## 🧩 Source Code Modules

### `modules/__init__.py`
**Type:** Python Package Initializer  
**Purpose:** Module package definition  
**Description:** Makes the modules directory a Python package, enabling imports of sentiment analyzer, priority scorer, data processor, and visualization components.

### `modules/sentiment_analyzer.py`
**Type:** Python Module  
**Purpose:** Sentiment analysis engine  
**Description:** Implements sentiment analysis using transformer models (BERT, RoBERTa, etc.). Analyzes customer feedback text and returns sentiment scores (positive, negative, neutral) with confidence levels.

### `modules/priority_scorer.py`
**Type:** Python Module  
**Purpose:** Priority calculation  
**Description:** Calculates priority scores for feedback items based on sentiment intensity, urgency keywords, customer tier, and configurable weights. Assigns priority levels (Critical, High, Medium, Low).

### `modules/data_processor.py`
**Type:** Python Module  
**Purpose:** Data processing and transformation  
**Description:** Handles data cleaning, normalization, validation, and transformation. Prepares raw feedback data for analysis and formats results for visualization.

### `modules/visualizations.py`
**Type:** Python Module  
**Purpose:** Data visualization  
**Description:** Creates interactive charts and graphs using Plotly, including sentiment distribution, priority breakdown, trend analysis, and category-wise insights.

---

## 🔌 Data Connectors

### `connectors/__init__.py`
**Type:** Python Package Initializer  
**Purpose:** Connector package definition  
**Description:** Makes the connectors directory a Python package, enabling imports of various data source connectors.

### `connectors/base_connector.py`
**Type:** Python Module  
**Purpose:** Abstract base connector  
**Description:** Defines the interface and common functionality for all data connectors. Ensures consistent API across different data sources.

### `connectors/csv_connector.py`
**Type:** Python Module  
**Purpose:** CSV file connector  
**Description:** Reads feedback data from CSV files. Supports file upload through Streamlit interface and local file system access.

### `connectors/sql_connector.py`
**Type:** Python Module  
**Purpose:** SQL database connector  
**Description:** Connects to SQL databases (PostgreSQL, MySQL, SQLite) to fetch feedback data. Supports parameterized queries and connection pooling.

### `connectors/mongodb_connector.py`
**Type:** Python Module  
**Purpose:** MongoDB connector  
**Description:** Connects to MongoDB databases to retrieve feedback documents. Handles NoSQL query operations and document transformation.

### `connectors/api_connector.py`
**Type:** Python Module  
**Purpose:** REST API connector  
**Description:** Fetches feedback data from external REST APIs. Supports authentication, pagination, and rate limiting.

---

## 🛠️ Utility Modules

### `utils/__init__.py`
**Type:** Python Package Initializer  
**Purpose:** Utilities package definition  
**Description:** Makes the utils directory a Python package for utility functions.

### `utils/export_handler.py`
**Type:** Python Module  
**Purpose:** Data export functionality  
**Description:** Handles exporting analysis results to various formats (CSV, Excel, JSON, PDF reports). Includes formatting and styling options.

---

## 📚 Documentation

### `README.md`
**Type:** Markdown Documentation  
**Purpose:** Project overview and setup guide  
**Description:** Main project documentation covering features, installation instructions, usage examples, and quick start guide. First file users should read.

### `QUICKSTART.md`
**Type:** Markdown Documentation  
**Purpose:** Quick start guide  
**Description:** Condensed guide for getting the application running quickly. Includes minimal setup steps and basic usage examples.

### `PROJECT_SUMMARY.md`
**Type:** Markdown Documentation  
**Purpose:** Project summary and architecture  
**Description:** High-level overview of project architecture, design decisions, technology stack, and system components.

### `DEPLOYMENT.md`
**Type:** Markdown Documentation  
**Purpose:** Deployment guide  
**Description:** Comprehensive deployment instructions for various platforms (Docker, Kubernetes, cloud services). Includes production configuration and best practices.

### `DEPLOYMENT_CHECKLIST.md`
**Type:** Markdown Documentation  
**Purpose:** Pre-deployment checklist  
**Description:** Step-by-step checklist to ensure all deployment requirements are met before going to production. Covers security, performance, and monitoring.

### `MANIFEST.md` (this file)
**Type:** Markdown Documentation  
**Purpose:** Project file inventory  
**Description:** Complete listing and description of all project files, their purposes, and relationships.

---

## 🚀 Deployment Files

### `Dockerfile`
**Type:** Docker Configuration  
**Purpose:** Container image definition  
**Description:** Defines the Docker image for the application. Includes base image, dependencies, application code, and runtime configuration. Optimized for production use.

### `docker-compose.yml`
**Type:** Docker Compose Configuration  
**Purpose:** Multi-container orchestration  
**Description:** Defines services, networks, and volumes for running the application with dependencies (databases, caching) in Docker containers.

### `k8s-deployment.yaml`
**Type:** Kubernetes Configuration  
**Purpose:** Kubernetes deployment specification  
**Description:** Defines Kubernetes resources (Deployment, Service, ConfigMap, Secrets) for deploying the application to Kubernetes clusters. Includes scaling and health check configurations.

---

## 📊 Data Files

### `data/sample_feedback.csv`
**Type:** CSV Data File  
**Purpose:** Sample dataset  
**Description:** Example customer feedback data for testing and demonstration. Contains sample feedback text, timestamps, customer IDs, and categories.

### `assets/`
**Type:** Directory  
**Purpose:** Static assets  
**Description:** Contains images, logos, icons, and other static files used in the application interface and documentation.

---

## 🔄 GitHub Workflows

### `.github/workflows/deploy.yml`
**Type:** GitHub Actions Workflow  
**Purpose:** CI/CD pipeline  
**Description:** Automated workflow for continuous integration and deployment. Runs tests, builds Docker images, and deploys to production on code changes.

---

## 📦 Export Scripts

### `export-project.ps1`
**Type:** PowerShell Script  
**Purpose:** Windows project export  
**Description:** PowerShell script for Windows users to create a timestamped ZIP archive of the entire project. Excludes unnecessary files (.git, cache, etc.) and provides detailed export summary.

**Usage:**
```powershell
.\export-project.ps1
.\export-project.ps1 -OutputDir "C:\Exports"
```

### `export-project.sh`
**Type:** Bash Script  
**Purpose:** Linux/Mac project export  
**Description:** Bash script for Linux and macOS users to create a timestamped ZIP archive of the project. Includes colored output, progress indicators, and automatic cleanup.

**Usage:**
```bash
chmod +x export-project.sh
./export-project.sh
./export-project.sh ~/exports
```

---

## 🔐 Streamlit Configuration

### `.streamlit/config.toml`
**Type:** TOML Configuration  
**Purpose:** Streamlit app configuration  
**Description:** Configures Streamlit application settings including theme, server options, browser behavior, and UI customization.

### `.streamlit/secrets.toml.example`
**Type:** TOML Template  
**Purpose:** Secrets template  
**Description:** Example file for storing sensitive configuration like API keys and database credentials. Users copy to `secrets.toml` and add actual secrets.

---

## 📁 Directory Structure

```
sentiment-analysis-triage/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml.example    # Secrets template
├── assets/                     # Static assets
├── connectors/                 # Data source connectors
│   ├── __init__.py
│   ├── api_connector.py
│   ├── base_connector.py
│   ├── csv_connector.py
│   ├── mongodb_connector.py
│   └── sql_connector.py
├── data/                       # Sample data
│   └── sample_feedback.csv
├── modules/                    # Core modules
│   ├── __init__.py
│   ├── data_processor.py
│   ├── priority_scorer.py
│   ├── sentiment_analyzer.py
│   └── visualizations.py
├── utils/                      # Utility functions
│   ├── __init__.py
│   └── export_handler.py
├── .dockerignore              # Docker exclusions
├── .env.example               # Environment template
├── .gitignore                 # Git exclusions
├── app.py                     # Main application
├── config.yaml                # Configuration
├── DEPLOYMENT_CHECKLIST.md    # Deployment checklist
├── DEPLOYMENT.md              # Deployment guide
├── docker-compose.yml         # Docker Compose config
├── Dockerfile                 # Docker image definition
├── export-project.ps1         # Windows export script
├── export-project.sh          # Linux/Mac export script
├── k8s-deployment.yaml        # Kubernetes config
├── MANIFEST.md                # This file
├── PROJECT_SUMMARY.md         # Project summary
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
└── requirements.txt           # Python dependencies
```

---

## 🎯 File Categories Summary

| Category | Count | Description |
|----------|-------|-------------|
| **Core Application** | 2 | Main app and dependencies |
| **Configuration** | 6 | Config files and templates |
| **Source Modules** | 8 | Python modules (4 core + 4 connectors) |
| **Utilities** | 2 | Helper functions and tools |
| **Documentation** | 6 | README, guides, and checklists |
| **Deployment** | 4 | Docker, K8s, and CI/CD configs |
| **Data** | 1 | Sample datasets |
| **Export Tools** | 2 | Export scripts for archiving |
| **Streamlit Config** | 2 | App configuration files |
| **Total Files** | 33+ | Complete project inventory |

---

## 📝 Notes

### Excluded from Exports
The export scripts automatically exclude the following:
- `.git/` - Git repository data
- `__pycache__/` - Python bytecode cache
- `venv/`, `env/`, `ENV/` - Virtual environments
- `node_modules/` - Node.js dependencies
- `.vscode/`, `.idea/` - IDE configurations
- `*.log` - Log files
- `.env` - Actual secrets (only `.env.example` included)
- Build artifacts and temporary files

### File Naming Conventions
- **Python files**: `snake_case.py`
- **Documentation**: `UPPERCASE.md` for important docs, `lowercase.md` for guides
- **Configuration**: Lowercase with extensions (`.yaml`, `.toml`, `.json`)
- **Scripts**: `kebab-case.sh` or `kebab-case.ps1`

### Version Control
All files listed in this manifest are tracked in Git except:
- Files matching patterns in `.gitignore`
- Sensitive files (`.env`, `secrets.toml`)
- Generated files (cache, logs, builds)

---

## 🔄 Maintenance

This manifest should be updated when:
- New files are added to the project
- File purposes or descriptions change significantly
- Major refactoring occurs
- New modules or features are introduced

**Last Review:** 2026-05-17  
**Next Review:** When significant changes occur

---

## 📞 Support

For questions about specific files or project structure:
1. Check the relevant documentation file (README.md, DEPLOYMENT.md, etc.)
2. Review inline code comments in source files
3. Consult the PROJECT_SUMMARY.md for architecture overview

---

*This manifest was generated as part of the project export package to provide a comprehensive overview of all project files and their purposes.*