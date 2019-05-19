from scipy import io
import pandas as pd

# a = io.loadmat('data/groundtruth.mat')['groundtruth'][0]
# files = []
# list_bboxes = []
# names = []
# for i in a:
#     file = i[0][0]
#     bboxes = i[1]
#     name = i[2][0]
#
#     files.append(file)
#     list_bboxes.append(bboxes)
#     names.append(name)


# df = pd.DataFrame({'file': files, 'bboxes': list_bboxes, 'name': names})
# df.to_json('data/data.json')

df = pd.read_json('data/data.json')
print(df.head())
print(df.shape)
b = df.loc[:, 'bboxes'].values


