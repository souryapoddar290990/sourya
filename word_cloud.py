from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = path.dirname(__file__)

text = open(path.join(d,'SmartBones.txt')).read()
# coi_coloring = np.array(Image.open(path.join(d,"dog.png")))
stopwords = set(STOPWORDS)
stopwordss = ['SmartBones','SmartBone','Five','Stars','loves','Five Stars','dog']
for item in stopwordss: stopwords.add(item.lower())

# wc = WordCloud(background_color="white", max_words=2000, mask=coi_coloring,stopwords=stopwords, max_font_size=20, random_state=42)
wc = WordCloud(background_color="white", max_words=75, stopwords=stopwords, max_font_size=20, random_state=42)
wc.generate(text)
# image_colors = ImageColorGenerator(coi_coloring)

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
# plt.figure()
# plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
# plt.axis("off")
# plt.figure()
# plt.imshow(coi_coloring, cmap=plt.cm.gray, interpolation="bilinear")
# plt.axis("off")
plt.show()

