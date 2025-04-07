# Genome Looker

Genome Looker is a web-based tool designed to compare genomic datasets using the Jaccard index. It allows users to upload BED files and find the most similar datasets from a predefined core database. The tool is built with FastAPI and provides a simple, intuitive interface for genomic comparison.

## Usage

1. Navigate to the application.
2. Upload a BED file for comparison.
3. View the top N most similar (Jaccard algorithm) datasets based on the Jaccard index.
4. Optionally save the uploaded dataset for future use or delete any existing datasets.
5. Use the interactive table to sort and filter results.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:vsem-azamat/genome-looker.git
   ```

2. Set up the `.env` file:
   ```bash
   cp .env.example .env
   ```
   You can keep the default values or modify them as needed. *(Default port is 8000.)*

3. Build and run the application:
   ```bash
   docker-compose up --build
   ```

4. Access the application at `http://localhost:8000`.

## API Endpoints

### OpenAPI Documentation
- The API documentation is available at `/docs` or `/redoc`.

### `/api/dataset/`
- **POST**: Upload a new dataset. Example payload: `{"file": file}`
- **GET**: Retrieve a specific dataset. Example: `{dataset}`
- **DELETE**: Delete a specific dataset. Example: `{dataset}`

### `/jaccards_html`
- **POST**: Calculate Jaccard similarity and return results as an HTML template.

## Technologies Used

- **FastAPI**
- **PyBedTools**
- **HTMLX**
- **Tabulator.js**
- **Jinja2**
- **Docker**

## Directory Structure

```
genome-looker/
├── backend/
│   ├── api/                # API routes
│   ├── core/               # Core configurations and dependencies
│   ├── pages/              # HTML page routes
│   ├── schemas/            # Pydantic models
│   ├── services/           # Business logic
│   ├── static/             # Static assets (CSS, JS, etc.)
│   ├── templates/          # HTML templates
│   ├── main.py             # FastAPI entry point
│   └── requirements.txt    # Python dependencies
├── tests/                  # Test suite
├── docker-compose.yml      # Docker configuration
├── .env                    # Environment variables
└── README.md               # Project documentation
```

## Future Improvements

- Add support for additional genomic file formats and archives.
- Integrate a database for persistent storage, enabling dataset and result retention for future reference.
- Optimize Jaccard similarity calculations for large datasets.
- Enhance the frontend for better interactivity and user experience, potentially migrating to React.
- Logging, if needed.
- More integration api and unit tests.
