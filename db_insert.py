import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    print("[*] Successfully connected to PostgreSQL.")

    try:
        print("[*] Setting up Engineering Domains...")
        # Upsert ensures we don't crash if the domain already exists
        cs_domain = await db.engineeringdomain.upsert(
            where={"name": "Computer Science"},
            data={
                "create": {"name": "Computer Science"},
                "update": {}
            }
        )

        print("[*] Injecting University and Syllabus data...")
        university = await db.university.upsert(
            where={"name": "Kamla Nehru Institute of Technology"},
            data={
                "create": {
                    "name": "Kamla Nehru Institute of Technology", 
                    "state": "Uttar Pradesh",
                    "syllabi": {
                        "create": [
                            {
                                "raw_text": "Introduction to Machine Learning using Python. Data handling with Pandas and SQL. Deployment basics using Docker. Linear Regression Mathematics.",
                                "domainId": cs_domain.id # Links the syllabus to the CS Domain
                            }
                        ]
                    }
                },
                "update": {}
            }
        )
        print(f"[+] Registered: {university.name} under {cs_domain.name}")

        print("[*] Injecting market job data...")
        job = await db.joblisting.create(
            data={
                "title": "Applied AI Engineer",
                "description": "Requires PyTorch, Docker, CI/CD, and ONNX deployment on edge devices.",
                "marketScore": 88.5,
                "domainId": cs_domain.id # Links the job to the CS Domain
            }
        )
        print(f"[+] Registered job: {job.title}")

    except Exception as e:
        print(f"[!] Database Operation Failed: {e}")
        
    finally:
        await db.disconnect()
        print("[*] Database connection safely closed.")

if __name__ == '__main__':
    asyncio.run(main())