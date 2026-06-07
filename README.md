Nexus Analytics Engine (EduGap Analyzer)

An enterprise-grade, full-stack data pipeline and visualization dashboard designed to mathematically expose the systemic gap between traditional academic engineering curricula and modern industry tooling requirements.

📌 The Problem
The global tech market moves at a rapid pace, demanding applied execution skills (Docker, AWS, React, Advanced FEA, BIM). However, traditional academic frameworks (such as the AICTE national baseline in India) remain largely focused on foundational theory.

This project was built to stop guessing and start measuring that exact deficit.

🚀 The Solution
Nexus Analytics is a multi-domain data engineering pipeline that:

Models Academic Baselines: Maps standard engineering syllabi across Computer Science, Mechanical, Civil, and Electronics branches.

Aggregates Market Demand: Calculates the real-world demand for specific industry tools (Python, Revit, SolidWorks, AutoCAD, etc.).

Computes the Deficit: Mathematically calculates the percentage of industry-required skills actually being taught in the classroom.

Visualizes the Reality: Serves the computed data through a high-performance, dark-mode React dashboard using responsive SVGs and data visualization libraries.

🏗️ Architecture Stack
Data & Backend Layer
Python 3: Core execution logic for data parsing and aggregation.

FastAPI: High-speed, asynchronous API framework serving the calculated metrics to the frontend.

PostgreSQL: Relational database ensuring strict data integrity.

Prisma (Python Client): Next-generation ORM handling database schema generation and strictly typed data transactions.

Frontend Presentation Layer
React.js: Component-based UI rendering.

Recharts: Composable charting library building the responsive Donut and Bar charts.

Pure CSS / Glassmorphism: Fluid, viewport-aware layout scaling seamlessly from mobile to ultra-wide monitors without relying on heavy UI libraries.

⚙️ Local Development & Setup
1. Database & Backend Configuration
Bash
# Clone the repository
git clone https://github.com/rajpatel2276/EduGap-Analyzer.git
cd EduGap-Analyzer

# Set up the Python Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install fastapi uvicorn prisma requests beautifulsoup4

# Push the schema to your local PostgreSQL instance
# (Ensure your DATABASE_URL is set in a local .env file)
prisma db push
prisma generate

# Seed the database with the national baseline and market metrics
python3 national_pipeline.py
python3 update_market.py

# Boot the API server
uvicorn api:app --reload
The API will now be running on http://localhost:8000

2. Frontend Configuration
Open a second terminal window:

Bash
# Navigate to the frontend directory (if separated) or root
npm install
npm install recharts

# Start the Vite development server
npm run dev
The Dashboard will be accessible at http://localhost:5173 (or port specified by Vite)

📂 Core Data Flow
update_market.py / national_pipeline.py: Ingests and structures raw market probabilities and academic text files, cleaning them for relational insertion.

Prisma ORM: Validates the payload and executes upsert commands into the PostgreSQL tables (University, EngineeringDomain, Syllabus, SkillKeyword).

api.py: FastAPI listens for frontend domain selections, queries the database, runs a Regex intersection analysis between syllabus text and market tools, and computes the final readiness_score.

App.jsx: React fetches the JSON payload, dynamically updates state, and renders the high-fidelity UI.

🛡️ License
Distributed under the MIT License. See LICENSE for more information.
