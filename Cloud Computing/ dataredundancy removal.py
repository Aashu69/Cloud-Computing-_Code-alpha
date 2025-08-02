import sqlite3
import hashlib

# ✅ Connect to or create a SQLite database
conn = sqlite3.connect('data_storage.db')
cursor = conn.cursor()

# ✅ Create a table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS data_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    hash TEXT UNIQUE NOT NULL
)
""")
conn.commit()

# ✅ Function to generate a unique hash for each entry
def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# ✅ Function to insert validated and unique data
def insert_data(data: str):
    hash_value = generate_hash(data.strip())

    # Check if hash already exists
    cursor.execute("SELECT * FROM data_entries WHERE hash = ?", (hash_value,))
    if cursor.fetchone():
        print("⚠️ Duplicate detected! Data not inserted.\n")
    else:
        cursor.execute("INSERT INTO data_entries (content, hash) VALUES (?, ?)", (data.strip(), hash_value))
        conn.commit()
        print("✅ Data inserted successfully.\n")

# ✅ Function to view current database entries
def view_entries():
    print("\n📋 Current Entries in Database:")
    cursor.execute("SELECT id, content FROM data_entries")
    rows = cursor.fetchall()
    if not rows:
        print("No data found.")
    for row in rows:
        print(f"{row[0]}. {row[1]}")
    print("-" * 50)

# ✅ Main menu for interaction
def main():
    while True:
        print("\n==== Data Redundancy Removal System ====")
        print("1. Insert New Data")
        print("2. View All Data")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            user_input = input("Enter new data: ")
            insert_data(user_input)
        elif choice == '2':
            view_entries()
        elif choice == '3':
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
