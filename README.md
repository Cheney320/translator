### 1 项目背景

- 构建一个较为完整的翻译器，首先识别输入文本的语种，在文本框输入文本，模型检测出语种，并在检测语言栏显示对应语种，接着选择翻译目标语言(默认为检测出的语种)，然后点击翻译按钮，对文本框输入的文本进行目标语言的翻译。大致参考谷歌翻译的功能，如下图所示：

![image-20200523175716731](https://tva1.sinaimg.cn/large/007S8ZIlgy1gf2jbljo7lj320k0d0wfl.jpg)



### 2 语种识别器建模

#### 2.1 数据介绍

来自twitter的数据，包含English, French, German, Spanish, Italian 和 Dutch(荷兰语) 6种语言，然后我又加入了中文句子(来源于爬取的新闻标题)。最终，每个语种的句子在1500条左右，数据较为均衡，数据分布如下图所示，

![image-20200603160328407](https://tva1.sinaimg.cn/large/007S8ZIlgy1gff5u0paz8j30dg0cw3z8.jpg)

其中

- ch:中文 
- en:英语 
- fr:法语
- it:意大利语
- de:德语
- es:西班牙语
- nl:荷兰语

#### 2.2 数据预处理

- 文本数据中发现包含网页链接、@人名，#话题名，数字及标点符号，且中文数据包含一些英文字母。这些都会对语种分类产生噪声影响。
- 因此，通过正则表达式对数据进行清洗，如下图所示：

![image-20200603160001641](https://tva1.sinaimg.cn/large/007S8ZIlgy1gff5qh8nvej31ig0mwgr0.jpg)

#### 2.3 文本向量化表示

一般来说，文本要进行向量化表示前要进行分词，英语等语言可通过空格进行分词，中文之间没有空格，可利用jieba等分词工具进行分词，向量化表示方法很多，比如词袋模型、N-gram模型、TF-IDF模型等。下面我们采用词袋模型(仅具有词频信息)，对于该语种分类任务来说，因为同属于拉丁语系的不同语言可能共享字母，通过单词的区分度可能不是很大，不同语言之间字母顺序可能是不同的，那么用字母作为划分颗粒度比较合适，再配合有词序的N-gram模型可以很好进行分类。我利用scikit-learn中的`CountVectorizer`实现，首先将文本中的字母全小写，再逐个字母解析，设置n-gram范围最高到3个连续字母。max_feature把所有的n-gram统计出的向量表排序取最高频的1000个，还可以加预处理函数，这里加入前面提及的数据清洗的函数。可以通过`vec.get_feature_names()`来查看这1000个词表，通过`toarray()`方法可获得文本的向量化表示。

```python
vec = CountVectorizer(
    lowercase=True,  # 英文文本全小写
    analyzer='char_wb',  # 逐个字母解析
    ngram_range=(1, 3),  # 1=出现的字母以及每个字母出现的次数，2=出现的连续2个字母，和连续2个字母出现的次数
    # trump images are now... => 1gram=t,r,u,m,p... 2gram=tr,ru,um,mp...
    max_features=1000,   # keep the most common 1000 ngrams
    preprocessor = remove_noise
)
vec.fit(X_train)
```

#### 2.4 模型训练与调优

`模型训练`：在获得的词向量模型基础上应用朴素贝叶斯模型进行分类，75%数据作为训练集，25%数据作为测试集

`调优`：主要就是对文本数据进行了清洗，去除了网页链接、@人名，#话题名，数字及标点符号，且中文数据包含一些英文字母。这个操作效果比较明显。

数据清洗前模型在测试集上预测准确率为0.9909159727479182，清洗后预测准确率达到0.9931869795609387

具体看每类的预测情况，文本清洗后中文和英文的预测效果都提升了1个百分点。

`清洗前`

![image-20200603164732811](https://tva1.sinaimg.cn/large/007S8ZIlgy1gff73vi3cwj30o40cit9y.jpg)

`清洗后`

![image-20200603164806565](https://tva1.sinaimg.cn/large/007S8ZIlgy1gff74gkrssj30oq0cgt9x.jpg)



#### 2.5 模型部署与应用

**代码规范化**

```python
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
```

**模型部署**

- 图形化界面方式

由于最近在学PyQt5，因此我采用PyQt5开发图形化界面程序，调用保存好的模型文件，在文本框中输入文本实时检测语种在状态栏显示语种信息。如下图所示：

![Jun-03-2020 17-01-07](https://tva1.sinaimg.cn/large/007S8ZIlgy1gff7jo4x43g30mc0co7wi.gif)

- Web应用





