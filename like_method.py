import pickle

class LikeDB:

    # like 수를 받아온다.
    def __init__(self):
        self.__file = open("like_value.txt", "rb+")
        self.__likeDic = pickle.load(self.__file) 
    
    def inc(self, item):
        # 'like' 수를 "like_value.txt"로부터 받아 like_dic의 값을 수정해준다.
        self.__likeDic[item] += 1
        print(self.__likeDic)
        
    def save(self):
        self.__file.seek(0)
        pickle.dump(self.__likeDic, self.__file)
        self.__file.seek(0)
        print(pickle.load(self.__file))
    
    def getLikes(self):
        return self.__likeDic
    
    def __del__(self):
        self.__file.close()

# likeDB 초기화
if __name__ == '__main__':
    f = open("like_value.txt", "wb+")
    pickle.dump({'clothes1': 0, 'clothes2': 0, 'clothes3': 0, 'clothes4': 0, 'clothes5': 0, 'clothes6': 0, 'clothes7': 0, 'clothes8': 0, 'clothes9': 0, 'clothes10': 0, 'clothes11': 0, 'clothes12': 0}, f)
    f.seek(0)
    pickle.loads(f)
    f.close()

