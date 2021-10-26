import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
#-------csv文件地址信息-------------------------------
user_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/tags.csv'
movie_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/movies.csv'
genre_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/movies.csv'
link_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/links.csv'
rating_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/ratings.csv'
tag_dir = '/home/lisha/PycharmProjects/zy/dazuoye/ml-25m/tags.csv'
#-----------------1、一共有多少不同用户--------------------
def user_number (dir):
    user_data = pd.read_csv(dir)  # 读取训练数据
    t=user_data.duplicated(subset=["userId"],keep=False)
    n_user=len(t[t==False])#False的个数即代表不重复的键的个数
    print("1.user_number is :",n_user)

#-----------------2、一共有多少不同电影--------------------
def movie_number (dir):
    movie_data = pd.read_csv(dir)  # 读取训练数据
    t=movie_data.duplicated(subset=["movieId"],keep=False)
    n_movie=len(t[t==False])#False的个数即代表不重复的键的个数
    print("2.movie_number is :",n_movie)

#-----------------3、一共有多少电影类型--------------------
def genre_number (dir):
    genre_data = pd.read_csv(dir)  # 读取训练数据
    genress = genre_data["genres"].str.split(pat="|")
    #print(aaaa[0].tail(20))
    genres = pd.Series([genre for _, genre_list in genress.items() for genre in genre_list],
                       name="genres")  # 所有体裁组成一个list（包含重复）
    genres = genres.unique().tolist()
    genres.remove('(no genres listed)')  # ! 认为没有题材不算一个题材，如果认为算，删掉此行即可
    print("3.genre_number is :",len(genres))

#-----------------4、没有外部链接的电影数-----------------------------
def link_number (link_dir,movie_dir):
    link_data = pd.read_csv(link_dir)  # 读取训练数据
    movie_data = pd.read_csv(movie_dir)
    he_data = pd.merge(link_data, movie_data)
    print("4.The number of movies without external links is :",(he_data["tmdbId"].isna().sum()+he_data["imdbId"].isna().sum()))

#-----------5、2018年对电影进行过评分的人数-----------------------------------------------
def rating_number (dir):
    rating_data = pd.read_csv(dir)  # 读取训练数据
    #print(rating_data.tail(20))
    start_time = datetime(2018, 1, 1, 0, 0).timestamp()
    end_time = datetime(2019, 1, 1, 0, 0).timestamp() - 1
    #time_data = rating_data.loc[(rating_data.timestamp >= 1514764800) & (rating_data.timestamp <= 1567850400)]
    time_data = rating_data.loc[(rating_data.timestamp >= start_time) & (rating_data.timestamp <= end_time)]
    t = time_data.duplicated(subset=["userId"], keep=False)
    n_time = len(t[t == False])
    print("5.taring_number in 2018 is :", n_time)
#-----------6、2018年评分5分以上的电影及其对应的标签-----------------------------------------------
def rating_number5 (dir,tag_dir):
    rating_data = pd.read_csv(dir)  # 读取训练数据
    #print(rating_data.tail(20))
    tag_data = pd.read_csv(tag_dir)  # 读取训练数据
    he_data = pd.merge(rating_data, tag_data)
    start_time = datetime(2018, 1, 1, 0, 0).timestamp()
    end_time = datetime(2019, 1, 1, 0, 0).timestamp() - 1
    #time_data = rating_data.loc[(rating_data.timestamp >= 1514764800) & (rating_data.timestamp <= 1567850400)]
    time_data = he_data.loc[(he_data.timestamp >= start_time) & (he_data.timestamp <= end_time)]
    #print(time_data.head(20))
    print("6.movies rated and label above 5 points in 2018 is : \n", time_data)
#-----------7、绘制电影复仇者联盟（The Avengers）每个月评分的平均值变化曲线图-----------------------------------------------
def avengers_score (dir,movie_dir):
    rating_data = pd.read_csv(dir)  # 读取训练数据
    movie_data = pd.read_csv(movie_dir)
    he_data = pd.merge(rating_data, movie_data)
    #print(he_data.head(20))
    avengers_data = he_data[he_data["title"].str.contains("Avengers")]
    avengers_data["data"] = pd.to_datetime(avengers_data['timestamp'],unit='s')
    avengers_data["month"] = avengers_data["data"].dt.month
    avengers_data.groupby(['month'])[["rating"]].mean().plot()
    plt.show()
    plt.savefig('/home/lisha/PycharmProjects/zy/dazuoye/rating.jpg')
if __name__ == "__main__":
    user_number (user_dir)
    movie_number (movie_dir)
    genre_number (genre_dir)
    link_number (link_dir,movie_dir)
    rating_number (rating_dir)
    rating_number5(rating_dir,tag_dir)
    avengers_score(rating_dir,movie_dir)

