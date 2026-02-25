from functions import write_file


def main():
    result = write_file.write_file("calculator", "lorem.txt", "wait, this isnt lorem ipsum")
    print(result)




if __name__ == "__main__":
    main()
