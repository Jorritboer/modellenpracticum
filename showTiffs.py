from PIL import Image
from os import listdir
from os.path import isfile, join
PATH = "/home/kevin/Documents/ModellenPracticum/modellenpracticum2023/.tiff_data"
tiffFiles = [join(PATH,f) for f in listdir(PATH) if isfile(join(PATH, f))]
firstImage = Image.open(tiffFiles[0])
for tiffFile in tiffFiles[1:]:
    print("ANOTHER ONE")
    foreground = Image.open(tiffFile)

    firstImage.paste(foreground, (0, 0), foreground)
firstImage.save(r'overLayedTiffs.tiff')