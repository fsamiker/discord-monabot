from PIL import Image, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import os

class ImageProcessor:

    BACKGROUND_SIZE = (4080, 3072)
    BACKGROUND_IMAGE = 'assets/genshin/namecards/galaxy.jpg'
    FONT = "assets/fonts/NotoSansJP-Bold.otf"
    IMAGE_REDUCTION_RATIO = 6
    IMAGE_OPTIMIZE = True
    IMAGE_QUALITY = 100  #Max = 100

    def __init__(self):
        pass

    def generate_character_info(self, character):
        # Size & Ratios
        text_color = (255, 255, 255, 255)

        ch_im_margin_ratio_h = 0.5
        ch_im_margin_ratio_w = 0.7

        el_im_size = (256, 256)
        el_im_margin_ratio = 0.15

        ch_name_margin_ratio_h = 0.18
        ch_name_margin_ratio_w = 0.2
        ch_font_size = 200

        rarity_star_size = (128, 128)
        rare_margin_ratio_h = 0.28
        rare_margin_ratio_w = 0.2
        rarity_icon = 'assets/genshin/icons/star.png'

        info_text_margin_ratio_h = 0.4
        info_text_spacing_ratio = 0.075
        info_text_margin_ratio_w = 0.2
        info_textwrap_w = 20
        info_font_size = 80
        icon_size = (128, 128)
        icon_margin_ratio_w = 0.15
        basic_info_icons = ['assets/genshin/icons/weapon.png',
        'assets/genshin/icons/region.png',
        'assets/genshin/icons/white_cake.png',
        'assets/genshin/icons/group.png',
        'assets/genshin/icons/food.png']

        # Check File Existence
        output_file = f'assets/genshin/generated/basic_info_{character.name}.png'
        if os.path.isfile(output_file):
            return output_file

        # Get Background Image
        im = Image.open(self.BACKGROUND_IMAGE).convert('RGBA')
        im = im.resize(self.BACKGROUND_SIZE, Image.NEAREST)

        # Insert Character Image
        try:
            ch_im = Image.open(character.get_portrait()).convert("RGBA")
            ch_im_height_ratio = 2600/ch_im.height
            ch_im_w = int(ch_im.width*ch_im_height_ratio)
        except:
            return
        ch_im = ch_im.resize((ch_im_w, 2600), Image.NEAREST)
        ch_w_placement = int(im.width*ch_im_margin_ratio_w-ch_im.width/2)
        ch_h_placement = int(im.height*ch_im_margin_ratio_h-ch_im.height/2)
        im.paste(ch_im, (ch_w_placement,ch_h_placement), ch_im)

        # Insert Element Icon
        el_im = Image.open(character.get_element_icon()).convert("RGBA")
        el_margin_w = int(im.width*el_im_margin_ratio)
        el_margin_h = int(im.height*el_im_margin_ratio)
        el_im = el_im.resize(el_im_size, Image.NEAREST)
        im.paste(el_im, (el_margin_w, el_margin_h), el_im)

        # Insert Character Name
        font = ImageFont.truetype(self.FONT, ch_font_size)
        ch_name_margin_w = int(im.width*ch_name_margin_ratio_w)
        ch_name_margin_h = int(im.height*ch_name_margin_ratio_h)
        draw = ImageDraw.Draw(im)
        draw.text((ch_name_margin_w, ch_name_margin_h), character.name, font=font, fill=text_color)

        # Insert Rarity Stars
        rarity_w = int(im.width*rare_margin_ratio_w)
        rarity_h = int(im.height*rare_margin_ratio_h)
        star_im = Image.open(rarity_icon).convert("RGBA")
        star_im = star_im.resize(rarity_star_size, Image.NEAREST)
        for _s in range(character.rarity):
            im.paste(star_im, (rarity_w, rarity_h), star_im)
            rarity_w += star_im.width

        # Insert Misc Information
        info_h = int(im.height*info_text_margin_ratio_h)
        icon_w = int(im.width*icon_margin_ratio_w)

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self.FONT, info_font_size)
        info = character.get_basic_info()
        for i in range(len(info)):
            icon = Image.open(basic_info_icons[i]).convert('RGBA').resize(icon_size, Image.NEAREST)
            im.paste(icon, (icon_w, info_h), icon)
            text = '\n'.join(textwrap.wrap(info[i], width=info_textwrap_w))   
            info_w = int(icon_w+icon.width*1.5)
            draw.text((info_w, info_h), text, font=font, fill=text_color)
            info_h += int(im.height*info_text_spacing_ratio)

        scaled_im = im.resize((int(im.width/self.IMAGE_REDUCTION_RATIO), int(im.height/self.IMAGE_REDUCTION_RATIO)), Image.ANTIALIAS)
        scaled_im.save(output_file, optimize=self.IMAGE_OPTIMIZE, quality=self.IMAGE_QUALITY)
        return output_file

    def generate_materials_needed(self, icon, title, resource, output_file):
        # Size & Ratios
        bg_size = (4080, 6120)
        bg_image = 'assets/genshin/namecards/galaxy3.jpg'
        text_color = (255, 255, 255, 255)

        main_icon_size = (256, 256)
        main_icon_margin_ratio_w = 0.05
        main_icon_margin_ratio_h = 0.025
        
        title_margin_ratio_w = 1.5
        title_margin_ratio_h = 0.25
        title_fontsize = 150

        mora_margin_ratio_w = 0.33
        mora_margin_ratio_h = 0.1
        mora_text_ratio_w = 1.5
        mora_text_ratio_h = 0.15
        mora_fontsize = 150

        mat_icon_size = (256, 256)
        mat_starting_ratio_w = 0.2
        mat_starting_ratio_h = 2
        mat_text_ratio_w = 1.2
        mat_text_ratio_h = 0.5
        mat_spacing_ratio_w = 3
        mat_spacing_ratio_h = 2
        mat_fontsize = 120

        btm_margin_ratio = 0.03

        # Check File Existence
        if os.path.isfile(output_file):
            return output_file

        # Get background image
        im = Image.open(bg_image).convert('RGBA')
        im = im.resize(bg_size, Image.NEAREST)

        # Insert Character Icon, Name, Title
        icon_im = Image.open(icon).convert("RGBA")
        icon_im = icon_im.resize(main_icon_size, Image.NEAREST)
        icon_w = int(im.width*main_icon_margin_ratio_w)
        icon_h = int(im.height*main_icon_margin_ratio_h)
        im.paste(icon_im, (icon_w, icon_w), icon_im)

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self.FONT, title_fontsize)
        draw.text((int(icon_w+icon_im.width*title_margin_ratio_w), int(icon_h+icon_im.height*title_margin_ratio_h)), title, font=font, fill=text_color)

        # Insert Mora
        mora_im = Image.open('assets/genshin/icons/i_Mora.png').convert('RGBA')
        mora_im = mora_im.resize((256, 256), Image.NEAREST)
        mora_h = int(im.height*mora_margin_ratio_h)
        mora_w = int(icon_w+im.width*mora_margin_ratio_w)
        im.paste(mora_im, (mora_w, mora_h), mora_im)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self.FONT, mora_fontsize)
        draw.text((int(mora_w+mora_im.width*mora_text_ratio_w), int(mora_h+mora_im.height*mora_text_ratio_h)), str(resource['Mora']), font=font, fill=text_color)


        # Insert Materials
        mat_starting_h = int(mora_h+mora_im.height*mat_starting_ratio_h)
        mat_starting_w = int(icon_w+im.width*mat_starting_ratio_w)
        i = 1
        w = mat_starting_w
        h = mat_starting_h
        next_h = h
        font = ImageFont.truetype(self.FONT, mat_fontsize)
        for key, count in resource['Materials'].items():
            mat_im = Image.open(f'assets/genshin/icons/i_{key}.png')
            mat_im = mat_im.resize(mat_icon_size, Image.NEAREST)
            im.paste(mat_im, (w, h), mat_im)
            draw = ImageDraw.Draw(im)
            draw.text((int(w+mat_im.width*mat_text_ratio_w), int(h+mat_im.height*mat_text_ratio_h)), f'x{str(count)}', font=font, fill=text_color)

            if i == 1:
                next_h = h+int(mat_im.height*mat_spacing_ratio_h)

            if i >= 3:
                i = 1
                w = mat_starting_w
                h = next_h
            else:
                i += 1
                w += int(mat_im.width*mat_spacing_ratio_w)
            
        # Crop Image
        final_h = int(next_h + im.height*btm_margin_ratio)
        im = im.crop((0, 0, im.width, final_h))

        scaled_im = im.resize((int(im.width/self.IMAGE_REDUCTION_RATIO), int(im.height/self.IMAGE_REDUCTION_RATIO)), Image.ANTIALIAS)
        scaled_im.save(output_file, optimize=self.IMAGE_OPTIMIZE, quality=self.IMAGE_QUALITY)
        return output_file