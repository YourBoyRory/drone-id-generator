import qrcode
import base64
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

class DroneTag:

    drone_ids = []
    drone_data=None
    drone_tag=None
    drone_id=None

    def __init__(self, drone_data={},  drone_ids=[]):
        self.drone_data = drone_data
        self.drone_ids = drone_ids
        name = drone_data.get("name", None)
        self.drone_id = self.drone_data.get("drone_id", None)
        if self.drone_id == None:
            if name != None:
                self.drone_id = self.generate_drone_id(name, self.drone_ids)
                self.drone_data["drone_id"] = self.drone_id
            else: return
        self.drone_ids.append(self.drone_id)


        drone_qr = self.place_qrcode_logo(self.generate_drone_qr(self.drone_data), self.drone_data)
        self.generate_drone_tag(drone_qr, self.drone_data)
        self.drone_data.pop("name", None)

    def save(self, path=None):
        if path == None and self.drone_id != None: path=f'{self.drone_id}.png'
        if path != None and self.drone_tag!= None: self.drone_tag.save(path)

    def place_qrcode_logo(self, qr_img, drone_data):
        logo = drone_data.get("logo", None)
        if logo == None:
            return qr_img
        else: logo = Image.open(logo)
        logo_mod = drone_data.get("logo_size", 0.2)
        logo_border = drone_data.get("logo_border", 0.2)
        border_radius = drone_data.get("border_radius", 0.125)
        front_color = drone_data.get("logo_color",
        tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        qr_img = qr_img.convert("RGBA")
        logo = logo.convert("RGBA")
        r, g, b, a = logo.split()
        logo = Image.new("RGBA", logo.size, (*front_color, 255))
        logo.putalpha(a)
        qr_w, qr_h = qr_img.size
        logo_size = int(qr_w*logo_mod)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pad = int(logo_size*logo_border)
        bg_size = logo_size + pad * 2
        bg = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        radius = int(bg_size*border_radius)
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

    def generate_drone_tag(self, qr_img, drone_data):
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        id_size = drone_data.get("id_size", None)
        title_size = drone_data.get("title_size", None)
        text = drone_data.get("drone_id", "")
        side_text = drone_data.get("title", "")
        new_img = qr_img
        if text != "":
            if id_size == None: font_size=81
            else: font_size=id_size
            margin=75
            font = ImageFont.truetype("./assets/font.otf", font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            while id_size == None and text_width <= qr_img.width - margin:
                font = ImageFont.truetype("./assets/font.otf", font_size)
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                font_size += 1
            text_height = bbox[3] - bbox[1]
            padding = text_height - 14
            new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
            draw = ImageDraw.Draw(new_img)
            text_x = (new_img.width - text_width) // 2
            draw.text((text_x, 20), text, fill=front_color, font=font)
            new_img.paste(qr_img, (0, text_height + padding))

        if side_text != "":
            qr_img = new_img.rotate(-90, expand=True)
            text = side_text
            if title_size == None: font_size=1
            else: font_size=title_size
            margin= 70 + ((text_height - text_height//2)//2)
            font = ImageFont.truetype("./assets/font.otf", font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            while title_size == None and text_width <= qr_img.width - margin:
                font = ImageFont.truetype("./assets/font.otf", font_size)
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                font_size += 1
            text_height = bbox[3] - bbox[1]
            padding = text_height - (text_height//2//2) + (len(text)//2)
            if any(ord(c) > 127 for c in text): padding = padding//2
            new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
            draw = ImageDraw.Draw(new_img)
            text_x = ((new_img.width) - text_width) // 2
            draw.text((text_x, 20), text, fill=front_color, font=font)
            new_img.paste(qr_img, (0, text_height + padding))
            new_img = new_img.rotate(90, expand=True)

        self.drone_tag = new_img
        return new_img

    def generate_drone_qr(self, drone_data):
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        data = self.drone_data.get("qr_data", self.drone_id)
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
            module_drawer=RoundedModuleDrawer(radius_ratio=1), # <-- adjust roundness here
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



"""
    EXAMPLE USAGE AND UNIT TEST
"""
if __name__ == "__main__":

    import os, json
    drone_ids = [
        os.path.splitext(f)[0]
        for f in os.listdir(".")
        if f.lower().endswith(".png")
    ]
    drone_ids = [] # Comment this out to enable loading drone name

    drones = [
        {
            "name": "Rory",
            "title": "Pup Drone",
            "front_color": "#DC141E",
        },
        {
            "drone_id": "#0000",
            "title": "Hexcorp",
            "logo": "./assets/hex2.png",
            "logo_size": 0.225,
            "logo_border": 0.133,
            "front_color": "#AB34C7",
        },
        {
            "name": "Website",
            "title": "Somename",
            "qr_data": "https://www.example.com/make_this_qr_code_massive_please",
            "front_color": "#FFA500",
        },
        {
            "name": "Long Text",
            "title": "Your Extra Long Text Here",
            "front_color": "#1E90FF",
        },
        {
            "name": "Short Text",
            "title": "s",
            "title_size": 80, # <-- This is needed for small text
            "front_color": "#1E90FF",
        },
        {
            "name": "Big Text",
            "title": "BIG TEXT",
            "title_size": 400,
            "front_color": "#1E90FF",
        },
        {
            "name": "Small Text",
            "title": "Small",
            "title_size": 30,
            "front_color": "#1E90FF",
        },
        {
            "This will": "get skipped"
        },
        {
            "name": "Rory",
            "qr_data": "https://www.example.com/",
            "front_color": "#34B134",
        },
        {
            "name": "Some Pokemon",
            "title": "Poké Drone",
            "logo": "./assets/rocket.png",
            "front_color": "#DC141E",
        }
    ]

    for drone in drones[:]:
        #drone_ids = [] # Uncomment this out to disable collision detection
        drone_tag = DroneTag(drone, drone_ids)
        print(f"Droneified: {drone_tag.drone_id} {json.dumps(drone_tag.drone_data, indent=4)}\n")
        if drone_tag.drone_id != None: drone_tag.save(f"./examples/{drone_tag.drone_id}.png")


