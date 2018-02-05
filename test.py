import queue,threadpool,threading,logging,traceback
from ReadCsv import ReadCsv
from youtubeDownLoad import youtubeDownLoad
from time import sleep

class Test():

    def __init__(self):
        self.pool = threadpool.ThreadPool(4)
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('logger.log')
        self.handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s'))
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def task(self,item):
        print(threading.current_thread(),item)
        sleep(7)

    def start(self):
        self.pool = threadpool.ThreadPool(4)
        temp = []
        for i in range(10):
            d = {}
            d['name'] = i
            d['load'] = 'lad'
            temp.append(d)
        requests = threadpool.makeRequests(self.task, temp)
        for req in requests:
            self.pool.putRequest(req)
        self.pool.wait()

    def check(self):
        i = -8
        while True:
            try:
                i = i + 1
                print(i)
                if i <= 0:
                    print(i / 0)
                print('ok')
                break
            except:
                print(i,'false')




if __name__ == '__main__':
    # youtu = youtubeDownLoad()
    # readcsv = ReadCsv()
    # readcsv.csv2dict('g:/class_labels_indices.csv', 1, 2)
    # readcsv.loadCsv('g:/eval_segments.csv', 4, 'd:/audioset', 0, 3)
    # items = readcsv.getItem()
    # temp = []
    # i = 0
    # for item in items:
    #     temp.append(item)
    #     i = i + 1
    #     if i > 6:
    #         break
    # print(len(temp))
    # pool = threadpool.ThreadPool(4)
    # requests = threadpool.makeRequests(youtu.download, temp)
    # for req in requests:
    #     pool.putRequest(req)
    # pool.wait()
    # print('all is over')
    test = Test()
    test.check()

