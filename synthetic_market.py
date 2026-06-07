import json
import random

def generate_market_data():
    print("[*] Generating 1,200 synthetic job records (Simulating Enterprise API Payload)...")
    
    domains = {
        "Computer Science": ["python", "sql", "pytorch", "docker", "aws", "react", "node"],
        "Mechanical Engineering": ["autocad", "solidworks", "ansys", "catia", "matlab", "fea"],
        "Civil Engineering": ["autocad", "revit", "staad", "etabs", "primavera", "gis"],
        "Electronics & Communication": ["matlab", "vlsi", "verilog", "iot", "embedded", "arduino"]
    }
    
    all_jobs = []
    
    # Generate 300 jobs for each domain
    for domain_name, skills in domains.items():
        for i in range(300):
            # Randomly pick 2 to 4 core skills for this specific job listing
            job_skills = random.sample(skills, k=random.randint(2, 4))
            
            # Occasionally mix in a cross-domain skill (e.g., a Mech Engineer needing Python)
            if random.random() > 0.8:
                job_skills.append("python")
                
            description_text = f"We are hiring a {domain_name}. The candidate must have experience in " + ", ".join(job_skills) + "."
            
            all_jobs.append({
                "source_domain": domain_name,
                "description": description_text
            })
            
    # Shuffle the jobs to simulate a real API feed
    random.shuffle(all_jobs)

    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=4)
        
    print(f"[+] Successfully wrote {len(all_jobs)} records to market_data.json.")

if __name__ == "__main__":
    generate_market_data()
