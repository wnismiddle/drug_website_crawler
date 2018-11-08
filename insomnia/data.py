import jieba
import jieba.posseg as jseg
jieba.load_userdict('dict/dict.txt')
import re
import os


f = open('dict/stoplist.txt', 'r', encoding='utf-8-sig')
stoplist = [line.strip() for line in f.readlines()]
# print(stoplist)


def generate_corpus():
    content = ''
    input_dir = 'result/'
    corpus_path = 'final_corpus.txt'
    nonsense_list = ['展开全部', '病情分析：', '指导意见：', '健康咨询描述：']
    with open(corpus_path, 'w', encoding='utf-8') as f_corpus:
        # 遍历爬取的各个来源的网页数据
        for parent, dirnames, filenames in os.walk(input_dir):
            for file in filenames:
                # 读取数据
                with open(os.path.join(parent, file), 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        if line == '\r' or line == '\n' or line.replace('\n', '').replace('\r', '').isspace():
                            continue
                        elif line.strip() in nonsense_list or len(line.strip()) < 2:
                            continue
                        content += line.strip()+'\n'
        # 汇总写入txt
        f_corpus.write(content)


def word2vec_pre():
    pattern = r'[？|。?!！；]'
    corpus_path = 'final_corpus.txt'
    word2vec_pre_path = 'word2vec_pre_opt.txt'
    with open(word2vec_pre_path, 'w', encoding='utf-8') as f_write:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # print(line)
                line_split = re.split(pattern, str(line))
                # print(line_split)
                for sentence in line_split:
                    reduce_wordlist = []
                    if sentence == '\r' or sentence == '\n' or len(sentence.strip()) == 1:
                        continue
                    wordlist = jieba.cut(sentence)
                    for word in wordlist:
                        if word in stoplist or word.isspace():
                            continue
                        else:
                            reduce_wordlist.append(word.strip())
                    if len(reduce_wordlist) > 1:
                        f_write.write(" ".join(reduce_wordlist) + '\n')

def make_sougou_dict():
    input_dir = 'scel2txt/'
    output_path = 'dict/dict.txt'
    f_write = open(output_path, 'w', encoding='utf-8')
    # parent - 父级目录 dirnames - 子目录  filenames - 文件名
    for parent, dirnames, filenames in os.walk(input_dir):
        print(parent, dirnames, filenames)
        for file in filenames:
            with open(os.path.join(parent, file), 'r', encoding='utf-8') as f:
                for line in f:
                    f_write.write(line)
    f_write.close()


if __name__ == '__main__':
    # make_sougou_dict()  # 合并搜狗医学、药物词库作为分词参考词典
    generate_corpus()   # 合并爬取关于“思诺思”的网页文本数据
    word2vec_pre()      # 对合并数据进行噪声过滤、分词、去除停用词处理，生成word2vec可训练的预处理文本

    # with open('dict/keyword.txt', 'r', encoding='utf-8') as f:
    #     with open('dict/keyword_dict.txt', 'w', encoding='utf-8') as f_write:
    #         for line in f.readlines():
    #             f_write.write(line.split('\t')[0]+'\n')

