import os
import re
import json
import subprocess

REGIONAL_SYLLABUS_PDF = "syllabus.pdf"

# =====================================================================
# THE INDIAN AI/ML MARKET BASELINE (2026)
# Based on India Skills Report & Entry-Level Job Portal Aggregations
# =====================================================================
INDIAN_TECH_DEMAND_MATRIX = {
    "Core Programming & Data Handling": {
        "keywords": [r"python", r"sql", r"pandas", r"numpy", r"data wrangling"],
        "market_weight": 95.0 # % of entry-level AI jobs requiring this
    },
    "Applied Machine Learning Frameworks": {
        "keywords": [r"pytorch", r"tensorflow", r"scikit-learn", r"keras", r"opencv", r"yolo"],
        "market_weight": 85.0
    },
    "Generative AI & Modern NLP": {
        "keywords": [r"llm", r"rag", r"langchain", r"prompt engineering", r"generative ai", r"transformers"],
        "market_weight": 70.0
    },
    "MLOps, Cloud & Deployment (The Execution Gap)": {
        "keywords": [r"docker", r"kubernetes", r"aws", r"gcp", r"mlflow", r"ci/cd", r"fastapi", r"model deployment"],
        "market_weight": 80.0
    },
    "Hardware Optimization & Edge AI": {
        "keywords": [r"onnx", r"quantization", r"tensorrt", r"edge ai", r"cuda"],
        "market_weight": 40.0
    }
}

def parse_local_syllabus_pdf():
    """Extracts raw text from your university's official PDF syllabus."""
    if not os.path.exists(REGIONAL_SYLLABUS_PDF):
        print(f"[!] '{REGIONAL_SYLLABUS_PDF}' not found in the current directory.")
        return ""
    
    print(f"[*] Extracting text matrix from {REGIONAL_SYLLABUS_PDF} via poppler-utils...")
    try:
        result = subprocess.run(["pdftotext", REGIONAL_SYLLABUS_PDF, "-"], capture_output=True, text=True, check=True)
        return result.stdout.lower()
    except Exception as e:
        print(f"[!] PDF extraction failed: {e}")
        return ""

def calculate_syllabus_coverage(text, matrix):
    """
    Scans the syllabus for the required Indian market skills.
    We calculate a 'coverage score' based on how many sub-skills in a category the syllabus actually teaches.
    """
    coverage_report = {}
    
    for category, data in matrix.items():
        matched_skills = 0
        total_skills = len(data["keywords"])
        
        for pattern in data["keywords"]:
            if re.search(pattern, text):
                matched_skills += 1
                
        # Calculate what percentage of the required toolset is actually taught
        coverage_percentage = (matched_skills / total_skills) * 100 if total_skills > 0 else 0
        coverage_report[category] = coverage_percentage
        
    return coverage_report

def run_indian_market_analysis():
    print("\n=== STARTING INDIAN AI/ML SYLLABUS AUDIT (2026 BASELINE) ===")
    
    syllabus_text = parse_local_syllabus_pdf()
    if not syllabus_text:
        print("[!] Cannot proceed without syllabus data. Please add 'syllabus.pdf'.")
        return
        
    print("[+] Syllabus ingested successfully. Computing alignment against Indian tech requirements...\n")
    
    academic_coverage = calculate_syllabus_coverage(syllabus_text, INDIAN_TECH_DEMAND_MATRIX)
    
    gap_report = {}
    overall_market_demand = 0
    overall_academic_coverage = 0
    
    for category, data in INDIAN_TECH_DEMAND_MATRIX.items():
        demand = data["market_weight"]
        coverage = academic_coverage[category]
        # The Delta is the missing capability: Market Demand minus what the school provided
        delta = max(0.0, demand - coverage)
        
        overall_market_demand += demand
        overall_academic_coverage += coverage
        
        gap_report[category] = {
            "Indian Industry Demand": f"{demand}%",
            "Syllabus Actual Coverage": f"{round(coverage, 1)}%",
            "Skill Deficit (Delta)": f"{round(delta, 1)}%"
        }
    
    # Calculate overall readiness
    total_categories = len(INDIAN_TECH_DEMAND_MATRIX)
    readiness_score = (overall_academic_coverage / overall_market_demand) * 100 if overall_market_demand > 0 else 0
    
    print("================== CURRICULUM VS. INDIAN MARKET GAP ==================")
    print(json.dumps(gap_report, indent=4))
    print("======================================================================")
    print(f">> OVERALL WORKFORCE READINESS SCORE: {round(readiness_score, 2)}%")
    print("======================================================================\n")

if __name__ == "__main__":
    run_indian_market_analysis()