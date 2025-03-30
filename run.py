from run_blind import try_blind_based
from run_union import try_union_based


def main():
    flag_found = try_union_based()
    if not flag_found:
        flag_found = try_blind_based()


if __name__ == "__main__":
    main()