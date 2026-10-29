# AI-Text-Analysis---Generation-Tool
# AI Text Analysis & Generation Tool

A full-stack Natural Language Processing (NLP) web application that combines **text summarization, plagiarism detection, semantic similarity analysis, and grammar correction** in a single interface.

Built with React.js, FastAPI, Python, MongoDB, and NLP models and tools, the project aims to simplify everyday text-processing tasks through an integrated web application.

**Repository:** [AI Text Analysis & Generation Tool](https://github.com/Aman-mishra-29/AI-Text-Analysis---Generation-Tool)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Structure](#database-structure)
- [Docker Setup](#docker-setup)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

## Project Overview

The AI Text Analysis & Generation Tool is designed to bring multiple text-processing capabilities together in one application. Users can submit text through a web interface, process it using the appropriate backend service, and view the resulting output.

The application follows a modular architecture in which the frontend manages user interactions, the backend exposes REST APIs, NLP services process the input, and MongoDB supports the storage and retrieval of processing history.

The main objective is to make common writing and text-analysis tasks more convenient, accessible, and manageable through a single platform.

## Features

### 1. Text Summarization

The summarization module generates shorter versions of longer text while attempting to preserve the original meaning and important information.

**Key capabilities:**
- Submit text for summarization.
- Generate abstractive summaries using a BART-based model.
- Configure summary length through request parameters.
- Display the generated summary and input/output text statistics.

**Model:** `facebook/bart-large-cnn`

### 2. Plagiarism Detection and Semantic Similarity Analysis

The plagiarism module compares a submitted text with one or more comparison texts and calculates similarity scores.

**Key capabilities:**
- Accept source text and comparison text.
- Generate semantic representations of text.
- Calculate similarity between the input and comparison texts.
- Return individual match scores and an overall similarity score.

The backend uses Sentence-BERT-related sentence embeddings and similarity calculations.

**Important:** Similarity scores are indicators for further investigation, not definitive proof of plagiarism. The results depend on the text supplied, the selected model, and the comparison method.

### 3. Grammar and Spelling Correction

The autocorrect module processes text to identify writing issues and provide corrections.

**Key capabilities:**
- Accept text for correction.
- Identify grammar and spelling issues using LanguageTool-based processing.
- Return corrected text.
- Provide correction details, including original text, suggested corrections, and explanatory messages where available.

### 4. History Dashboard

The dashboard provides an interface for reviewing previously processed results.

The backend history API retrieves recent records from the summarization, plagiarism, and autocorrect MongoDB collections.

The history endpoint currently limits each collection query to the ten most recent records.

### 5. REST API Integration

The frontend communicates with the FastAPI backend through HTTP requests using Axios.

The backend provides:
- Request validation.
- Dedicated endpoints for text-processing operations.
- Structured JSON responses.
- Request logging and error handling.
- Interactive API documentation through Swagger UI.

### 6. Document Input

The frontend includes document-processing dependencies such as `mammoth` and `pdfjs-dist`, intended to support Word and PDF document handling. Supported file types and limitations depend on the implementation of the document-upload component.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, JavaScript |
| Routing | React Router |
| API communication | Axios |
| Styling | Tailwind CSS, PostCSS |
| Frontend build tool | Vite |
| Backend | Python, FastAPI |
| Data validation | Pydantic |
| ASGI server | Uvicorn |
| Text summarization | Hugging Face Transformers, BART |
| Semantic similarity | Sentence Transformers, embeddings, similarity calculations |
| Grammar correction | LanguageTool |
| Database | MongoDB |
| Database connectivity | PyMongo |
| Containerization | Dockerfile for the backend |
| API testing | FastAPI Swagger UI |

## System Architecture

The application separates the user interface, API layer, processing services, and database operations.

```text
                    USER
                     |
                     v
              REACT FRONTEND
            React.js + Axios
                     |
                     | HTTP / JSON
                     v
               FASTAPI BACKEND
                     |
          +----------+----------+
          |          |          |
          v          v          v
     SUMMARIZATION PLAGIARISM AUTOCORRECT
          |          |          |
          v          v          v
         BART     Sentence     LanguageTool
                  Embeddings
                     |
                     v
              MONGODB DATABASE
                     |
                     v
              HISTORY DASHBOARD
```

### Workflow

1. The user enters text or provides a supported document.
2. The React frontend sends a request to the backend.
3. FastAPI validates the request and calls the appropriate service.
4. The relevant NLP model or processing tool handles the text.
5. The backend returns the processing result to the frontend.
6. Results are displayed in the interface.
7. Processing history is stored or retrieved through MongoDB where the corresponding persistence logic is implemented.

## Project Structure

The repository is organized into the following main directories and files.

```text
AI-Text-Analysis---Generation-Tool/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── history.py
│   │   ├── db/
│   │   │   └── mongo.py
│   │   ├── models/
│   │   │   ├── request_models.py
│   │   │   └── response_models.py
│   │   ├── routes/
│   │   │   ├── summarize.py
│   │   │   ├── plagiarism.py
│   │   │   └── autocorrect.py
│   │   ├── services/
│   │   │   ├── summarizer.py
│   │   │   ├── plagiarism_engine.py
│   │   │   └── autocorrect_engine.py
│   │   ├── utils/
│   │   │   ├── preprocessing.py
│   │   │   └── similarity.py
│   │   ├── config.py
│   │   └── main.py
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   └── mongo_schema.js
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   └── tailwind.config.js
│
├── .gitignore
└── README.md
```

The Dockerfile is currently named `dockerfile` in the repository. Rename it to `Dockerfile` if you want to follow the usual naming convention.

## Prerequisites

Install the following software before running the application:

- **Python 3.10:** The backend Dockerfile uses Python 3.10.
- **Node.js and npm:** Required to install and run the React frontend.
- **MongoDB:** Required for database-backed history and other database operations.
- **Git:** Required to clone the repository.
- **Internet connection:** May be required to download Python packages and NLP model files.

Model loading and inference can require substantial memory and disk space, depending on the machine and the models used.

## Installation and Setup

### Step 1: Clone the repository

Open PowerShell or a terminal and run:

```powershell
git clone https://github.com/Aman-mishra-29/AI-Text-Analysis---Generation-Tool.git
cd AI-Text-Analysis---Generation-Tool
```

### Step 2: Create a Python virtual environment

From the repository root, run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

Install the backend dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

### Step 3: Configure the backend environment

Create a local environment file from the example:

```powershell
Copy-Item backend\.env.example backend\.env
```

Open `backend/.env` and use the variable names expected by `backend/app/config.py`.

For a typical local MongoDB installation, the relevant settings are:

```dotenv
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=text_ai_db
SUMMARIZATION_MODEL=facebook/bart-large-cnn
```

Adjust these values to match your local configuration. The backend currently expects `MONGO_URI`, rather than `MONGODB_URI`.

Do not commit `backend/.env` to GitHub.

### Step 4: Install frontend dependencies

Open a second terminal at the repository root:

```powershell
cd frontend
npm install
```

Make sure the dependency manifest is named `package.json` in lowercase. The repository currently lists it as `Package.json`; rename it before relying on npm or Linux-based environments.

### Step 5: Configure the frontend API URL

The frontend example environment file contains:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Create a local file from the example if needed:

```powershell
Copy-Item .env.example .env
```

Check that the API URL matches the backend address and route prefixes in your configuration. Vite environment variables are exposed to browser code when prefixed with `VITE_`, so never store private credentials in frontend environment variables.

## Running the Application

The application requires MongoDB, the FastAPI backend, and the React frontend to be running.

### Terminal 1: Start MongoDB

On Windows, if MongoDB has been installed as a Windows service, open an Administrator terminal and run:

```cmd
net start MongoDB
```

If MongoDB is already running, you do not need to start it again. Otherwise, start it using your installation's configured method.

### Terminal 2: Start the FastAPI backend

From the project root, activate the virtual environment and install dependencies as described above.

Then run:

```powershell
cd backend
uvicorn app.main:app --reload
```

The backend should start at:

- API base address: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- Swagger documentation: http://127.0.0.1:8000/docs
- ReDoc documentation: http://127.0.0.1:8000/redoc

Keep the backend terminal open.

### Terminal 3: Start the React frontend

Open a new terminal:

```powershell
cd "B:\text ai tool\frontend"
npm run dev
```

If you cloned the repository to another location, navigate to that location instead.

Open the local address displayed by Vite. The default is commonly:

http://localhost:5173

Keep the frontend terminal open while using the application.

## API Endpoints

The backend currently registers the following principal endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Returns the API welcome message and feature list |
| GET | `/health` | Checks whether the API is running |
| POST | `/api/v1/summarize/` | Generates a text summary |
| POST | `/api/v1/plagiarism/` | Compares text and returns similarity results |
| POST | `/api/v1/autocorrect/` | Returns corrected text and correction details |
| GET | `/history/` | Retrieves recent processing history |

The summarization request accepts text and optional summary length parameters. The plagiarism request accepts an input text and comparison texts. The autocorrect request accepts text for correction.

Use Swagger UI at `/docs` to inspect the current request models, response schemas, validation requirements, and available operations.

**Integration note:** The frontend currently configures its API base URL with the `/api/v1` prefix and requests history under that prefix. The backend currently registers the history router at `/history/`, outside that prefix. Align the frontend history request or backend route registration if the dashboard cannot retrieve history.

## Database Structure

The database connection is configured through the backend settings, using MongoDB and PyMongo.

The backend defines three principal collections:

| Collection | Purpose |
|---|---|
| `summaries` | Stores summarization history |
| `plagiarism` | Stores plagiarism/similarity analysis history |
| `autocorrect` | Stores autocorrect results and history |

The `database/mongo_schema.js` file contains the project's MongoDB schema-related setup.

The history API retrieves recent records from these collections, sorted by creation time and limited to ten records per collection.

Ensure MongoDB is running and that the configured URI and database name are correct before using database-backed features.

## Docker Setup

The repository includes a Dockerfile for the FastAPI backend.

Docker must be installed and running before using these commands.

From the backend directory, build the image:

```powershell
cd backend
docker build -f dockerfile -t ai-text-tool-backend .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 ai-text-tool-backend
```

The backend container listens on port 8000. This command alone does not start MongoDB or the React frontend.

For database-backed operation, configure the MongoDB connection so the container can reach the database. A `localhost` address inside a container refers to that container itself, not automatically to MongoDB running on the host machine.

The Dockerfile is a starting point for backend containerization; validate environment settings, database connectivity, and model downloads before using it for deployment.

## Troubleshooting

### Backend dependencies are missing

Activate the virtual environment and install the declared dependencies:

```powershell
pip install -r backend\requirements.txt
```

If running the command from inside `backend`, use:

```powershell
pip install -r requirements.txt
```

### MongoDB connection fails

- Confirm that MongoDB is running.
- Verify `MONGO_URI` in `backend/.env`.
- Verify the database name and network connection.
- Check the backend terminal for connection errors.

### Frontend cannot reach the API

- Confirm the backend is running.
- Open `http://127.0.0.1:8000/docs` to verify that the API starts.
- Check `VITE_API_BASE_URL` and the endpoint path.
- Check CORS settings and the browser developer console.

### npm cannot find the project manifest

Ensure the frontend manifest is named `package.json`, not `Package.json`, then run `npm install` again from the `frontend` directory.

### The first NLP request is slow

The model may need to download its files or initialize before performing inference. Check the backend terminal, internet connection, free disk space, and available memory.

### Dashboard history is missing

Confirm that MongoDB is available and that the backend history route matches the path requested by the frontend. See the [API Endpoints](#api-endpoints) section.

## Security Considerations

- Never commit `.env` files, passwords, access tokens, or production database credentials.
- Keep `venv/`, `node_modules/`, private data, local database dumps, and downloaded model weights out of version control.
- Use restricted CORS origins instead of wildcard origins for production deployments.
- Review uploaded documents and logs before sharing them publicly.
- Treat text similarity scores as indicators for review, not definitive plagiarism judgments.

## Future Enhancements

Potential improvements include:

- Multilingual text processing.
- Expanded document-format support.
- Downloadable reports and result exports.
- User authentication and user-specific history.
- Automated backend and frontend tests.
- More comprehensive evaluation datasets and documented performance metrics.
- Improved container orchestration and deployment configuration.

These items represent possible future work and should not be treated as implemented unless the corresponding functionality is present in the codebase.

## Author

**Aman Mishra**

- GitHub: [Aman-mishra-29](https://github.com/Aman-mishra-29)
- LinkedIn: [Aman Mishra](https://www.linkedin.com/in/aman-mishra-479973281)

If you encounter an issue, check the project configuration and terminal output first. When opening a GitHub issue, include the steps to reproduce the problem and the relevant error message. Remove credentials and personal data from logs before sharing them.
