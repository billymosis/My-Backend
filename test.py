import os

def start():
    if os.path.exists("./temp") is False:
        os.mkdir("./temp")



if __name__ == "__main__":
    start()