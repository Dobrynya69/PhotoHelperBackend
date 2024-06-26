from PIL import Image, ImageOps


class UserImageUtils():
    def borderize_image(image, color):     
        width, height = image.size
        edited_image = image
        if width > height:
            edited_image = Image.new(image.mode, [width, width], color)
            edited_image.paste(image, [0, (width - height) // 2])
            edited_image = ImageOps.expand(edited_image, width // 25, color)
        elif width < height:
            edited_image = Image.new(image.mode, [height, height], color)
            edited_image.paste(image, [(height - width) // 2, 0])
            edited_image = ImageOps.expand(edited_image, height // 25, color)
        else:
            edited_image = ImageOps.expand(edited_image, width // 25, color)

        edited_image.format = image.format
        return edited_image