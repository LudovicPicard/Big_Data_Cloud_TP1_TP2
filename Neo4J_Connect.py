from neo4j import GraphDatabase
import csv

uri = "bolt://localhost:7687"
user = "neo4j"
password = "avml94710"

driver = GraphDatabase.driver(uri, auth=(user, password))

def clean_int(value):
    """Convertit proprement un nombre ou renvoie None."""
    if value is None:
        return None
    v = value.replace(",", "").replace("$", "").strip()
    if v == "":
        return None
    try:
        return int(v)
    except:
        return None

def import_data():
    with driver.session() as session:

        print("🧨 Clearing database...")
        session.run("MATCH (n) DETACH DELETE n")

        print("📥 Importing Marvel & DC movies from db.csv...")

        with open("mcu_data/db.csv", encoding="latin-1") as f:
            reader = csv.DictReader(f)

            for row in reader:

                # Nettoyage des valeurs
                title = row["Original Title"].strip()
                company = row["Company"].strip() if row["Company"] else None
                rate = float(row["Rate"]) if row["Rate"] else None
                metascore = clean_int(row["Metascore"])
                minutes = clean_int(row["Minutes"])
                release = row["Release"].strip() if row["Release"] else None
                budget = clean_int(row["Budget"])
                opening_usa = clean_int(row["Opening Weekend USA"])
                gross_usa = clean_int(row["Gross\xa0USA"])
                gross_world = clean_int(row["Gross Worldwide"])

                session.run("""
                    CREATE (m:Movie {
                        title: $title,
                        company: $company,
                        rate: $rate,
                        metascore: $metascore,
                        minutes: $minutes,
                        release: $release,
                        budget: $budget,
                        opening_weekend_usa: $opening_usa,
                        gross_usa: $gross_usa,
                        gross_worldwide: $gross_world
                    })
                """, {
                    "title": title,
                    "company": company,
                    "rate": rate,
                    "metascore": metascore,
                    "minutes": minutes,
                    "release": release,
                    "budget": budget,
                    "opening_usa": opening_usa,
                    "gross_usa": gross_usa,
                    "gross_world": gross_world
                })

        print("✅ Import complete!")

if __name__ == "__main__":
    import_data()
