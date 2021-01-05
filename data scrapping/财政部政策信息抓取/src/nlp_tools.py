import matplotlib.pyplot as plt
import wordcloud 


def word_cloud(word_list,title="wordcloud"):

    word_string = " ".join(word_list)
    word_cloud = wordcloud.WordCloud(font_path='src/SourceHanSans-Regular.ttc').generate(word_string)

    plt.figure(figsize=(20,10))
    plt.imshow(word_cloud)
    plt.savefig(title)








