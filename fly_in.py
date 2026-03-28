import os
from visualiser.tvisual import TVisual


def main() -> None:
    print("Welcome to fly-in!")

    app = TVisual()
    app.run()


def list_files(path):
    for file in os.listdir("./maps"):
        print(file)

    # def list_dir(path: str):
    #     for root, dirs, files in os.walk(path):
    #         for file in files:
    #             print(f"{file}")


def list_dir(path: str):
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from list_dir(entry.path)
        elif entry.is_file() and entry.path.endswith(".txt"):
            yield entry.path


if __name__ == "__main__":
    main()

    # for blah in list_dir("./maps/"):
    #     print(blah)
