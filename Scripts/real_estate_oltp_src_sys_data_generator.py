import pyodbc
from faker import Faker
import random

# -------------------------------
#  Connect to SQL Server (Windows Auth)
# -------------------------------
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\MSSQLSERVER02;'
    'DATABASE=real_estate_src_oltp_sys;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

cursor.execute("SELECT GETDATE()")
print("Connection test:", cursor.fetchone())

# -------------------------------
#  Faker setup
# -------------------------------
fake = Faker('en_US')
Faker.seed(42)
random.seed(42)

# -------------------------------
#  Settings / Options
# -------------------------------
cities = ['Cairo', 'Giza', 'Alex', 'cairo', 'Gza']
status_options = ['Done', 'completed', 'DONE']
property_type_names = ['Apartment', 'Villa', 'Office', 'Shop']

# Generate lists of names for diversity
first_names = [fake.first_name() for _ in range(50)]
last_names  = [fake.last_name() for _ in range(50)]

# -------------------------------
# 2️⃣ Property Types (if empty)
# -------------------------------
cursor.execute("SELECT COUNT(*) FROM Property_Types")
if cursor.fetchone()[0] == 0:
    for type_name in property_type_names:
        cursor.execute("""
            INSERT INTO Property_Types (type_name)
            VALUES (?)
        """, type_name)
    conn.commit()
    print("[OK] Property Types inserted")

# Get valid property_type_ids from database
cursor.execute("SELECT property_type_id FROM Property_Types")
property_types_ids = [row[0] for row in cursor.fetchall()]
print(f"Using {len(property_types_ids)} property types: {property_types_ids}")

# -------------------------------
# 3️⃣ Customers (1000 rows)
# -------------------------------
for _ in range(1000):
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"
    
    email = None if random.random() < 0.1 else f"{first.lower()}.{last.lower()}@gmail.com"
    phone = None if random.random() < 0.1 else fake.msisdn()[0:11]
    city = random.choice(cities)
    
    cursor.execute("""
        INSERT INTO Customers (full_name, phone, email, city, last_updated)
        VALUES (?, ?, ?, ?, GETDATE())
    """, full_name, phone, email, city)

conn.commit()
print("[OK] Customers inserted")

# -------------------------------
# 4️⃣ Agents (50 rows)
# -------------------------------
for _ in range(50):
    first = random.choice(first_names)
    last = random.choice(last_names)
    agent_name = f"{first} {last}"
    
    phone = None if random.random() < 0.1 else fake.msisdn()[0:11]
    hire_date = fake.date_between(start_date='-5y', end_date='today')
    
    cursor.execute("""
        INSERT INTO Agents (agent_name, phone, hire_date, created_date, last_updated)
        VALUES (?, ?, ?, GETDATE(), GETDATE())
    """, agent_name, phone, hire_date)

conn.commit()
print("[OK] Agents inserted")

# -------------------------------
#  Properties (500 rows)
# -------------------------------
for _ in range(500):
    prop_type = random.choice(property_types_ids)
    city = random.choice(cities)
    price = None if random.random() < 0.1 else random.randint(50000, 5000000)
    area = random.randint(20, 500)
    
    cursor.execute("""
        INSERT INTO Properties (property_type_id, city, price, area_sq_m, created_date, last_updated)
        VALUES (?, ?, ?, ?, GETDATE(), GETDATE())
    """, prop_type, city, price, area)

conn.commit()
print("[OK] Properties inserted")

# -------------------------------
#  Transactions (2000 rows)
# -------------------------------
# Get valid IDs from database for foreign keys
cursor.execute("SELECT property_id FROM Properties")
property_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT customer_id FROM Customers")
customer_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT agent_id FROM Agents")
agent_ids = [row[0] for row in cursor.fetchall()]

print(f"Available IDs - Properties: {len(property_ids)}, Customers: {len(customer_ids)}, Agents: {len(agent_ids)}")

if len(property_ids) == 0 or len(customer_ids) == 0 or len(agent_ids) == 0:
    print("ERROR: Missing required data. Cannot insert transactions.")
else:
    for _ in range(2000):
        property_id = random.choice(property_ids)
        customer_id = random.choice(customer_ids)
        agent_id = random.choice(agent_ids)
        trans_date = fake.date_between(start_date='-2y', end_date='today')
        total_amount = None if random.random() < 0.1 else random.randint(100000, 5000000)
        status = random.choice(status_options)
        
        cursor.execute("""
            INSERT INTO Transactions (property_id, customer_id, agent_id, transaction_date, total_amount, status, created_date, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
        """, property_id, customer_id, agent_id, trans_date, total_amount, status)
    
    conn.commit()
    print("[OK] Transactions inserted")

# -------------------------------
#  Close connection
# -------------------------------
cursor.close()
conn.close()
print("[OK] All done! Realistic messy data inserted successfully.")
