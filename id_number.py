import qrcode
import base64
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask



class DroneTag:

    def __init__(self, name, color, drone_type, qr_data="", logo=""):
        front_color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = (1, 1, 1)

        self.drone_id = self.generate_drone_id(name)
        if qr_data == "": qr_data = self.drone_id
        self.drone_qr = self.generate_drone_qr(qr_data, front_color, back_color)
        if logo != "":
            logo_color = front_color #(220, 20, 30)
            logo = Image.open(logo)
            self.drone_qr = self.place_qrcode_logo(self.drone_qr, logo, logo_color, back_color)
        self.drone_tag = self.generate_drone_tag(self.drone_qr, self.drone_id, drone_type+" DRONE", front_color, back_color)

    def save(self, path=None):
        path=f'{self.drone_id}.png'
        self.drone_tag.save(path)

    def place_qrcode_logo(self, qr_img, logo, front_color, back_color):
        qr_img = qr_img.convert("RGBA")
        logo = logo.convert("RGBA")
        r, g, b, a = logo.split()
        logo = Image.new("RGBA", logo.size, (*front_color, 255))
        logo.putalpha(a)
        qr_w, qr_h = qr_img.size
        logo_size = int(qr_w*0.188)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pad = logo_size // 4
        bg_size = logo_size + pad * 2
        bg = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        radius = bg_size // 8   # <-- adjust roundness here
        print(radius)
        draw.rounded_rectangle(
            (0, 0, bg_size, bg_size),
            radius=radius,
            fill=(*back_color, 255),
        )
        bg_x = (qr_w - bg_size) // 2
        bg_y = (qr_h - bg_size) // 2
        logo_x = (qr_w - logo_size) // 2
        logo_y = (qr_h - logo_size) // 2
        qr_img.paste(bg, (bg_x, bg_y), bg)
        qr_img.paste(logo, (logo_x, logo_y), logo)

        return qr_img.convert("RGB")

    def generate_drone_tag(self, qr_img, text, side_text, front_color, back_color):
        font_size=81
        margin=75
        font = ImageFont.truetype("./assets/font.otf", font_size)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        while text_width <= qr_img.width - margin:
            font = ImageFont.truetype("./assets/font.otf", font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            font_size += 1
        text_height = bbox[3] - bbox[1]
        padding = 40
        new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
        draw = ImageDraw.Draw(new_img)
        text_x = (new_img.width - text_width) // 2
        draw.text((text_x, padding/2), text, fill=front_color, font=font)
        new_img.paste(qr_img, (0, text_height + padding))

        qr_img = new_img.rotate(-90, expand=True)
        text = side_text
        font_size=1
        margin=80
        font = ImageFont.truetype("./assets/font.otf", font_size)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        while text_width <= qr_img.width - margin:
            font = ImageFont.truetype("./assets/font.otf", font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            font_size += 1
        text_height = bbox[3] - bbox[1]
        padding = 40
        new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
        draw = ImageDraw.Draw(new_img)
        text_x = ((new_img.width) - text_width) // 2
        draw.text((text_x, padding/2), text, fill=front_color, font=font)
        new_img.paste(qr_img, (0, text_height + padding))

        return new_img.rotate(90, expand=True)

    def generate_drone_qr(self, data, front_color, back_color):
        qr = qrcode.QRCode(
            version=None,  # auto size
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(radius_ratio=0.8), # <-- adjust roundness here
            eye_drawer=RoundedModuleDrawer(radius_ratio=1),      # <-- adjust roundness here
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=front_color,
            ),
        )
        return qr_img.convert("RGB")

    def generate_drone_id(self, name, ids=[]):
        name = name.upper()
        base_number=(ord(name[0]) // 10) * 10
        id_number=f"0{ord(name[0])%10}-"
        temp=""
        if len(name) < 2: name+=name
        for i in name[1:]:
            temp+=str(abs(ord(i)-base_number))
        temp = f"{int(temp)%10000}"
        while int(temp) < 1000: temp+="0"
        id_number+=f"{temp}"
        while id_number in ids: id_number = str(int(id_number[0])+1) + id_number[1:]
        return id_number

if __name__ == "__main__":
    name="Rory"
    animal="Pup"
    qr_data = ""
    logo="./assets/logo.png"
    color = "#DC141E" #DC141E

    drone_tag = DroneTag(name, color, animal, qr_data, logo)
    drone_tag.save()


