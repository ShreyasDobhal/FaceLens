from PIL import Image, ExifTags
from paths import TEMP_FILE_PATH

tempFile = TEMP_FILE_PATH


def preprocessImage(filename):
    from PIL import Image

    
    try : 
        if filename[filename.rfind('.')+1:] not in ['jpg','jpeg']:
            im = Image.open(filename)
            rgb_im = im.convert('RGB')
            rgb_im.save(tempFile)
    except:
        pass
    try :
        image=Image.open(filename)
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(image._getexif().items())
        if   exif[orientation] == 3 : 
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            image=image.rotate(90, expand=True)
        image.save(tempFile)
    except:
        image.save(tempFile)
    

