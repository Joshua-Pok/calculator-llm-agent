from functions import run_python_file


def main():
    result = run_python_file.run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)


if __name__ == "__main__":
    main()
