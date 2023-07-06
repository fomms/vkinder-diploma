class PeopleIterator:
    '''Класс для итерирования по списку'''
    def __init__(self, list_):
        self.list_ = list_
        self.flag = True

    def __iter__(self):
        self.start = -1
        self.end = len(self.list_)
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            self.flag = False
            raise StopIteration
        else:
            return self.list_[self.start]