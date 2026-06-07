import asyncio
import json
import re
from prisma import Prisma

DOMAIN_MATRIX = {
    "Computer Science": ["python", "sql", "pytorch", "docker", "aws", "react", "node"],
    "Mechanical Engineering": ["autocad", "solidworks", "ansys", "catia", "matlab", "fea"],
    "Civil Engineering": ["autocad", "revit", "staad", "etabs", "primavera", "gis"],
    "Electronics & Communication": ["matlab", "vlsi", "verilog", "iot", "embedded", "arduino"]
}

async def update_clean_database():
    print("[*] Booting Production Market Engine...")
    
    try:
        with open('market_data.json', 'r') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("[!] market_data.json missing.")
        return

    total_jobs = len(jobs)
    db = Prisma()
    await db.connect()
    
    try:
        for domain_name, keywords in DOMAIN_MATRIX.items():
            # Guarantee the domain exists and get its ID
            domain = await db.engineeringdomain.upsert(
                where={"name": domain_name},
                data={"create": {"name": domain_name}, "update": {}}
            )

            # Filter jobs belonging to this domain to get an accurate localized weight
            domain_jobs = [j for j in jobs if j.get('source_domain') == domain_name]
            domain_total = len(domain_jobs)

            for kw in keywords:
                # Count occurrences within this domain's listings
                count = sum(1 for job in domain_jobs if re.search(kw, job.get('description', '')))
                market_weight = (count / domain_total) * 100 if domain_total > 0 else 0
                clean_term = kw.replace(r"\b", "")

                # STAKEHOLDER FIX: Upsert instead of Create to prevent row multiplication
                # We use a composite fluid check or unique matching based on your schema design
                # If your schema does not have a unique constraint on term+domainId, we delete old matching entries first
                await db.skillkeyword.delete_many(where={"term": clean_term, "domainId": domain.id})
                
                # Only insert active market demands to avoid zero-pollution
                if market_weight > 0:
                    await db.skillkeyword.create(
                        data={
                            "category": "Market Scraped Data",
                            "term": clean_term,
                            "marketWeight": round(market_weight, 2),
                            "domainId": domain.id
                        }
                    )
                    print(f"   -> {domain_name} | {clean_term.upper()}: {round(market_weight, 1)}%")
            
        print("[+] Database sanitized and synchronized perfectly.")
    except Exception as e:
        print(f"[!] Database Error: {e}")
    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(update_clean_database())