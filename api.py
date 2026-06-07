from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
import re

app = FastAPI(title="EdTech Market Gap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Prisma()

@app.on_event("startup")
async def startup():
    await db.connect()
    print("[*] FastAPI connected to PostgreSQL.")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/api/dashboard/national/{domain_name}")
async def get_dashboard_data(domain_name: str):
    try:
        domain = await db.engineeringdomain.find_first(where={"name": domain_name})
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found.")

        market_keywords = await db.skillkeyword.find_many(where={"domainId": domain.id})
        
        # Fetch our new National Average entity
        university = await db.university.find_first(
            where={"name": "Indian Academic Average (AICTE Standard)"},
            include={"syllabi": {"where": {"domainId": domain.id}}}
        )

        chart_data = []
        total_market = 0
        total_syllabus = 0
        latest_snippet = "No curriculum data logged."

        if university and university.syllabi:
            syllabus_text = university.syllabi[-1].raw_text.lower()
            latest_snippet = f"Curriculum baseline established. Systemic evaluation active."

            for kw in market_keywords:
                is_taught = bool(re.search(r"\b" + re.escape(kw.term) + r"\b", syllabus_text))
                syllabus_coverage = kw.marketWeight if is_taught else 0

                chart_data.append({
                    "name": kw.term.upper(),
                    "market": kw.marketWeight,
                    "syllabus": syllabus_coverage
                })

                total_market += kw.marketWeight
                total_syllabus += syllabus_coverage

        readiness_score = round((total_syllabus / total_market) * 100, 1) if total_market > 0 else 0

        return {
            "entity_name": "Indian Engineering System",
            "domain_name": domain.name,
            "latest_syllabus_snippet": latest_snippet,
            "readiness_score": readiness_score,
            "chart_data": sorted(chart_data, key=lambda x: x["market"], reverse=True)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        domain = await db.engineeringdomain.find_first(where={"name": domain_name})
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found.")

        market_keywords = await db.skillkeyword.find_many(where={"domainId": domain.id})
        
        university = await db.university.find_first(
            where={"name": university_name},
            include={"syllabi": {"where": {"domainId": domain.id}}}
        )

        if not university:
             raise HTTPException(status_code=404, detail="University not found.")

        chart_data = []
        total_market = 0
        total_syllabus = 0
        
        syllabus_text = ""
        # FIX: Cleaned up the "garbage" text logic
        latest_snippet = "No curriculum data logged for this department."

        if university.syllabi:
            syllabus_text = university.syllabi[-1].raw_text.lower()
            latest_snippet = f"Curriculum parsed. Document length: {len(syllabus_text)} characters. Semantic analysis complete."

        for kw in market_keywords:
            is_taught = bool(re.search(r"\b" + re.escape(kw.term) + r"\b", syllabus_text))
            syllabus_coverage = kw.marketWeight if is_taught else 0

            chart_data.append({
                "name": kw.term.upper(),
                "market": kw.marketWeight,
                "syllabus": syllabus_coverage
            })

            total_market += kw.marketWeight
            total_syllabus += syllabus_coverage

        readiness_score = round((total_syllabus / total_market) * 100, 1) if total_market > 0 else 0

        return {
            "university_name": university.name,
            "domain_name": domain.name,
            "latest_syllabus_snippet": latest_snippet,
            "readiness_score": readiness_score,
            "chart_data": sorted(chart_data, key=lambda x: x["market"], reverse=True)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        # 1. Fetch the requested Engineering Domain
        domain = await db.engineeringdomain.find_first(where={"name": domain_name})
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found in database.")

        # 2. Fetch the pristine market metrics we generated
        market_keywords = await db.skillkeyword.find_many(where={"domainId": domain.id})
        
        # 3. Fetch Kamla Nehru Institute's latest syllabus for this domain (if it exists)
        university = await db.university.find_first(
            where={"name": "Kamla Nehru Institute of Technology"},
            include={"syllabi": {"where": {"domainId": domain.id}}}
        )

        chart_data = []
        total_market = 0
        total_syllabus = 0
        latest_snippet = "No syllabus uploaded for this domain yet."

        syllabus_text = ""
        if university and university.syllabi:
            syllabus_text = university.syllabi[-1].raw_text.lower()
            latest_snippet = syllabus_text[:150] + "..."

        # 4. Calculate the gap based ONLY on database metrics
        for kw in market_keywords:
            # Check if the market-demanded skill is taught in the university syllabus
            is_taught = bool(re.search(r"\b" + re.escape(kw.term) + r"\b", syllabus_text))
            syllabus_coverage = kw.marketWeight if is_taught else 0

            chart_data.append({
                "name": kw.term.upper(),
                "market": kw.marketWeight,
                "syllabus": syllabus_coverage
            })

            total_market += kw.marketWeight
            total_syllabus += syllabus_coverage

        # Calculate final readiness score
        readiness_score = round((total_syllabus / total_market) * 100, 1) if total_market > 0 else 0

        return {
            "university_name": university.name if university else "Kamla Nehru Institute of Technology",
            "domain_name": domain.name,
            "latest_syllabus_snippet": latest_snippet,
            "readiness_score": readiness_score,
            "chart_data": sorted(chart_data, key=lambda x: x["market"], reverse=True) # Sort highest demand first
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))