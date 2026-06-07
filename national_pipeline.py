import asyncio
from prisma import Prisma

# The true baseline of Indian Engineering Curriculums (AICTE / State Averages)
NATIONAL_BASELINE = {
    "Computer Science": "C programming, object oriented programming in C++ and Java. Data structures and algorithms. Operating systems, computer networks, and theory of computation. Database management systems using basic SQL. Software engineering principles.",
    "Mechanical Engineering": "Engineering graphics, thermodynamics, fluid mechanics and machinery. Strength of materials, kinematics of machines, manufacturing processes, heat and mass transfer. Basic autocad drawing.",
    "Civil Engineering": "Surveying, building materials and construction. Structural analysis, geotechnical engineering, environmental engineering, fluid mechanics, transportation engineering. Basic drafting.",
    "Electronics & Communication": "Network analysis, electronic devices and circuits. Digital logic design, signals and systems, microprocessors and microcontrollers. Analog and digital communication systems. Basic matlab."
}

async def build_national_database():
    print("[*] Booting Realistic National Baseline Pipeline...")
    
    db = Prisma()
    await db.connect()
    
    try:
        # Clear out the old fake universities and syllabi to clean the database
        await db.syllabus.delete_many()
        await db.university.delete_many()

        domains = await db.engineeringdomain.find_many()
        if not domains:
            print("[!] Run update_market.py first to create domains.")
            return

        # Create the single, unified National Average entity
        uni = await db.university.create(
            data={
                "name": "Indian Academic Average (AICTE Standard)", 
                "state": "National"
            }
        )
        print(f"\n[*] Establishing Baseline: {uni.name}")

        for domain in domains:
            text_content = NATIONAL_BASELINE.get(domain.name, "")
            
            await db.syllabus.create(
                data={
                    "raw_text": text_content.lower(),
                    "universityId": uni.id,
                    "domainId": domain.id
                }
            )
            print(f"   -> Mapped realistic curriculum limits for {domain.name}.")
                
        print("\n[+] National Architecture reset and grounded in reality.")
        
    except Exception as e:
        print(f"[!] Database Error: {e}")
    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(build_national_database())
