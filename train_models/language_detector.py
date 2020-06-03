import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import os


class LanguageDetector():
    # 成员函数
    def __init__(self, classifier=MultinomialNB()):
        self.classifier = classifier
        self.vectorizer =  CountVectorizer(
                        lowercase=True,  # 英文文本全小写
                        analyzer='char_wb',  # 逐个字母解析
                        ngram_range=(1, 3),  # 1=出现的字母以及每个字母出现的次数，2=出现的连续2个字母，和连续2个字母出现的次数
                        # trump images are now... => 1gram=t,r,u,m,p... 2gram=tr,ru,um,mp...
                        max_features=1000,   # keep the most common 1000 ngrams
                        preprocessor = self._remove_noise
                    )

    # 私有函数，数据清洗
    def _remove_noise(self, document):
        noise_pattern = re.compile("|".join(["http\S+", "\@\w+", "\#\w+", "\d+", "，", "！", "。", '“', '”', "？", "\.+"]))
        clean_text = re.sub(noise_pattern, "", document)

        return clean_text.strip()

    # 特征构建
    def features(self, X):
        return self.vectorizer.transform(X)

    # 拟合数据
    def fit(self, X, y):
        self.vectorizer.fit(X)
        self.classifier.fit(self.features(X), y)

    # 预估类别
    def predict(self, x):
        return self.classifier.predict(self.features([x]))

    # 测试集评分
    def score(self, X, y):
        return self.classifier.score(self.features(X), y)

    # 模型持久化存储
    def save_model(self, path):
        dump((self.classifier, self.vectorizer), path)

    # 模型加载
    def load_model(self, path):
        self.classifier, self.vectorizer = load(path)

# 清理中文中的英文字母
def clean_chinese(document):
    pattern = re.compile('[A-Za-z]')
    clean_text = re.sub(pattern, "", document)
    return clean_text.strip()

if __name__ == '__main__':
    data = pd.read_csv('../data/new_data.csv', encoding='utf8')
    # 对中文数据进行清洗
    data.loc[data['nl'] == 'ch', '1 december wereld aids dag voorlichting in zuidafrika over bieten taboes en optimisme'] = \
    data.loc[data['nl'] == 'ch', '1 december wereld aids dag voorlichting in zuidafrika over bieten taboes en optimisme'].apply(
        lambda x: clean_chinese(x))
    # 切分数据集
    X, y = data['1 december wereld aids dag voorlichting in zuidafrika over bieten taboes en optimisme'], data['nl']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=666)
    language_detector = LanguageDetector()
    language_detector.fit(X_train, y_train)
    # # 保存模型
    dir = '../models/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = dir + 'language_detector.model'
    language_detector.save_model(path)
    # 模型预测
    language_detector.load_model(path)
    print(language_detector.predict('This is an English sentence'))
    print(language_detector.predict('你好呀！美女！！！'))
    print(language_detector.score(X_test, y_test))
