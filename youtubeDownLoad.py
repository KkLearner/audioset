import threadpool,youtube_dl,shutil,logging,traceback
from ReadCsv import ReadCsv

class youtubeDownLoad():

    def __init__(self,poolsize,proxy=None,quiet=True):
        self.pool = threadpool.ThreadPool(poolsize)
        self.logger = logging.getLogger()
        self.handler = logging.FileHandler('logger.log')
        self.handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s'))
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        self.proxy = proxy
        self.quiet = quiet

    def download(self,item):
        i = 1
        info = {'outtmpl': item['outtmpl'], 'quiet': self.quiet}
        if self.proxy:
            info['proxy'] = self.proxy
        while i <= 30:
            try:
                with youtube_dl.YoutubeDL(info) as ydl:
                    ydl.add_default_info_extractors()
                    res = ydl.extract_info(item['url'])
                    self.logger.info('rowNumber :%s %s is success in %s time(s)',item['rowNumber'],item['id'],i)
                    id = res.get('id')
                    ext = res.get('ext')
                    for road in item['desPath']:
                        shutil.copyfile(item['orilPath'] + id + '.' + ext, road + id + '.' + ext)
                        self.logger.info('rowNumber :%s copy to %s is ok in %s time(s)',item['rowNumber'], road,i)
                break
            except Exception as e:
                if i <= 3:
                    self.logger.error('rowNumber :%s %s is error %s in %s time(s)',item['rowNumber'],item['id'],traceback.format_exc(),i)
                    self.logger.warning('rowNumber :%s %s is retrying in %s time(s)',item['rowNumber'],item['id'],i)
                i = i + 1

    def start(self,labels_file,labels_keyindex,labels_valueindex,
              segments_file,start,outPutRootPath,ytid_index,positive_labels_index):
        readcsv = ReadCsv()
        readcsv.csv2dict(labels_file, labels_keyindex, labels_valueindex)
        readcsv.loadCsv(segments_file, start, outPutRootPath, ytid_index, positive_labels_index)
        item = readcsv.getItem()
        requests = threadpool.makeRequests(self.download, item)
        for req in requests:
            self.pool.putRequest(req)
        self.pool.wait()

if __name__ == '__main__':
    youtu = youtubeDownLoad(8)
    youtu.start('class_labels_indices.csv', 1, 2,'eval_segments.csv', 4, './audioset/eval', 0, 3)
    youtu.start('class_labels_indices.csv', 1, 2, 'balanced_train_segments.csv', 4, './audioset/balanced_train', 0, 3)
