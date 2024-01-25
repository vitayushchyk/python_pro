def main():
    search_term = input("Enter string for search: ")
    count = 0
    with open("rockyou.txt", "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if search_term in line:
                count += 1
    print(f"Search term {search_term} was found {count} times")


if __name__ == "__main__":
    main()
