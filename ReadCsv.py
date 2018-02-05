import csv,re,os
class ReadCsv(object):

    def __init__(self):
        self.__midToLabel = {}
        self.__item = []

    def csv2dict(self,in_file,keyindex,valueindex):
        with open(in_file) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.__midToLabel[row[keyindex]] = row[valueindex]
            f.close()

    def __clear(self):
        self.__item.clear()

    def loadCsv(self,in_file,start,rootRoad, ytid_index,positive_labels_index):
        with open(in_file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            i = 0
            self.__clear()
            for row in readCSV:
                i = i + 1
                if i < start:
                    continue
                name = re.sub(r'"|\s', '', row[positive_labels_index])
                video = {}
                video['id'] = row[ytid_index]
                video['rowNumber'] = i
                video['orilPath'] = rootRoad + '/{parent}/'.format(parent=self.__midToLabel[name])
                video['outtmpl'] = rootRoad + '/{parent}/%(id)s.%(ext)s'.format(
                    parent=self.__midToLabel[name])
                video['url'] = 'https://youtu.be/%s' % (row[ytid_index])
                count = len(row)
                desPath = []
                if count > positive_labels_index+1:
                    for j in range(count - positive_labels_index-1):
                        des = rootRoad+'/%s/' % (self.__midToLabel[re.sub(r'"|\s', '', row[j + positive_labels_index+1])])
                        desPath.append(des)
                        if not os.path.exists(des):
                            os.makedirs(des)
                video['desPath'] = desPath
                self.__item.append(video)
            csvfile.close()

    def getMidToLabel(self):
        return self.__midToLabel

    def getItem(self):
        return self.__item
