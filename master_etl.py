import asyncio
import subprocess
import os
import re
from prisma import Prisma

REGIONAL_SYLLABUS_PDF = "syllabus.pdf"

# The extraction targets
INDIAN_TECH_DEMAND_MATRIX = {
    "Core Programming": [r"python", r"sql", r"pandas", r"numpy"],
    "Applied ML": [r"pytorch", r"tensorflow", r"opencv", r"yolo"],
    "MLOps & Deployment": [r"docker", r"kubernetes", r"aws", r"fastapi"],
    "Edge AI": [r"onnx", r"quantization", r"tensorrt"]
}

def extract_pdf_text():
    if not os.path.exists(REGIONAL_SYLLABUS_PDF):
        return "Missing Syllabus Data. Ensure syllabus.pdf is in the directory."
    try:
        result = subprocess.run(["pdftotext", REGIONAL_SYLLABUS_PDF, "-"], capture_output=True, text=True, check=True)
        return result.stdout.lower()
    except:
        return "Extraction Failed"

def calculate_coverage(text):
    coverage_data = {}
    for category, keywords in INDIAN_TECH_DEMAND_MATRIX.items():
        matches = sum(1 for kw in keywords if re.search(kw, text))
        coverage_data[category] = (matches / len(keywords)) * 100 if keywords else 0
    return coverage_data

async def run_pipeline():
    print("[*] Booting Master ETL Pipeline...")
    
    print(f"[*] Extracting raw data from {REGIONAL_SYLLABUS_PDF}...")
    raw_text = extract_pdf_text()
    
    print("[*] Transforming unstructured text into coverage metrics...")
    metrics = calculate_coverage(raw_text)
    overall_score = sum(metrics.values()) / len(metrics) if metrics else 0
    
    print("[*] Loading calculated metrics into PostgreSQL...")
    db = Prisma()
    await db.connect()
    
    try:
        # 1. Guarantee the Domain exists before assigning it
        cs_domain = await db.engineeringdomain.upsert(
            where={"name": "Computer Science"},
            data={
                "create": {"name": "Computer Science"},
                "update": {}
            }
        )

        # 2. Guarantee the University exists
        university = await db.university.upsert(
            where={"name": "Kamla Nehru Institute of Technology"},
            data={
                "create": {"name": "Kamla Nehru Institute of Technology", "state": "Uttar Pradesh"},
                "update": {}
            }
        )
        
        # 3. Log the latest syllabus, passing BOTH the required IDs
        await db.syllabus.create(
            data={
                "raw_text": raw_text,
                "universityId": university.id,
                "domainId": cs_domain.id  # <-- This is the exact fix for your error
            }
        )
        
        print(f"[+] Successfully loaded data for {university.name} under {cs_domain.name}.")
        print(f"[+] Computed Institutional Coverage Score: {round(overall_score, 2)}%")
        
    except Exception as e:
        print(f"[!] Database Error: {e}")
    finally:
        await db.disconnect()
        print("[*] Pipeline execution complete. Database secured.")

if __name__ == '__main__':
    asyncio.run(run_pipeline())