import urllib2 as urllib
from cStringIO import StringIO
from PIL import Image


class ImageRenderer:

    def __init__(self, screenSize):
        self.image = None
        self.screenSize = screenSize

    def convert_image(self, image):
        # TODO: converion
        # TODO: error, if conversion fails
        try:
            rgb_image = image.convert("RGB")
        except:
            "unable to convert image to RGBA format"
            return False

        return rgb_image

    def get_new_size(self, image, screen_width, screen_height):
        img_width, img_height = image.size
        # returns new image h/w to fit screen
        img_ratio = img_width / img_height
        screen_ratio = screen_width / screen_height
        if screen_ratio > img_ratio:
            return (img_width * screen_height / img_height, screen_height)
        else:
            return (screen_width, img_height * screen_width / img_width)

    def get_frames(self, image):
        # cycle through and return rendered frames, handles animated images
        frames = []
        frames.append(image)
        while 1:
            try:
                image.seek(image.tell() + 1)
                frames.append(image)
            except EOFError:
                return frames

    def fetch_image(self, url):
        print('loadImage %s' % url)
        image_load_ok = None
        try:
            img_file = urllib.urlopen(url)
            im = StringIO(img_file.read())
            self.image = Image.open(im)
            self.image.load()
        except:
            print("Print fetching the image failed")
        # TODO : fetch remote image
        return self.image

    def getFrameCount(self, image):
        return 1

    def get_queue_token(self, msgToken):
        queue_token = {}
        print("get_queue_token got an msgToken")
        print(msgToken)
        # TODO: add possible params
        image = self.fetch_image(msgToken["url"])
        new_size = self.get_new_size(image, self.screenSize[0], self.screenSize[1])
        images = [
            image.convert("RGBA").resize(new_size)
            for image in self.get_frames(image)
        ]

        queue_token["image"] = images
        queue_token["frame_count"] = len(images)
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token

    def getImage(self):
        return self.image