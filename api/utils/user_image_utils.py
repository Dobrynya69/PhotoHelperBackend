from PIL import Image, ImageOps, ImageEnhance

from io import BytesIO
from django.core.files import File

class UserImageUtils():
    def __init__(self, model_object, image_name) -> None:
        self.model_object = model_object
        self.image_name = image_name
    
    def update_user_image(self):
        edited_image = Image.open(self.model_object.original_image)
        format = edited_image.format.capitalize()
        if self.model_object.contrast_value != 0:
            edited_image = self.change_image_contrast(edited_image, 1.0 + self.model_object.contrast_value / 100)
            
        if self.model_object.brightness_value != 0:
            edited_image = self.change_image_brightness(edited_image, 1.0 + self.model_object.brightness_value / 100)
            
        if self.model_object.is_borderized:
            edited_image = self.borderize_image(edited_image)
        
        io_image = BytesIO()
        edited_image.save(io_image, format=format)
        file_image = File(io_image, self.image_name)
        self.model_object.image.delete(True)
        self.model_object.image.save(self.image_name, file_image, True)
    
    def borderize_image(self, image):        
        width, height = image.size
        if width > height:
            edited_image = Image.new(image.mode, [width, width], 'white')
            edited_image.paste(image, [0, (width - height) // 2])
            edited_image = ImageOps.expand(edited_image, width // 10, 'white')
        elif width < height:
            edited_image = Image.new(image.mode, [height, height], 'white')
            edited_image.paste(image, [(height - width) // 2, 0])
            edited_image = ImageOps.expand(edited_image, height // 10, 'white')
        else:
            edited_image = ImageOps.expand(edited_image, width // 10, 'white')

        return edited_image

    def change_image_contrast(self, image, contrast_value):
        return ImageEnhance.Contrast(image).enhance(contrast_value)
    
    def change_image_brightness(self, image, brightness_value):
        return ImageEnhance.Brightness(image).enhance(brightness_value)