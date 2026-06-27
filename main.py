from workers.WebWorker import WebWorker


def main():
    w1=WebWorker()
    w1.start()
    w1.join()

if(__name__=="__main__"):
    main()
    
