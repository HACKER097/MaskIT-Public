import pyimgur

CLIENT_ID = ""
CLIENT_SECRET = ""

def ImageUploader(path):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path)
    return uploaded_image.link 
