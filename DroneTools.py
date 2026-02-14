from PIL import Image, ImageDraw, ImageFont

class HandlerBadge():
    pass

class DroneTag():

    drone_ids = []
    drone_data=None
    drone_tag=None
    drone_id=None

    def __init__(self, drone_data={},  drone_ids=[]):

        # Set variables
        self.drone_data = drone_data
        self.drone_ids = drone_ids
        name = drone_data.get("name", None)
        self.drone_id = self.drone_data.get("drone_id", None)

        # Generate ID number
        if self.drone_id == None:
            if name != None:
                self.drone_id = self.generate_drone_id(name, self.drone_ids)
                self.drone_data["drone_id"] = self.drone_id
            else: return # if the user provided nothing, well just return. Maybe they just wanna use the functions.
        self.drone_ids.append(self.drone_id)

        # Generate Code
        if self.drone_data.get("barcode", False):
            drone_code = self.generate_drone_barcode(self.drone_data)
        else:
            drone_code = self.place_qrcode_logo(self.generate_drone_qr(self.drone_data), self.drone_data)

        # Construct Tag
        self.generate_drone_tag(drone_code, self.drone_data)

        # delete the name, it is no longer needed.
        self.drone_data.pop("name", None)

    def save(self, path=None):
        if path == None and self.drone_id != None: path=f'{self.drone_id}.png'
        if path != None and self.drone_tag!= None: self.drone_tag.save(path)
    def get_image(self):
        return self.drone_tag

    def generate_drone_tag(self, code_img, drone_data):

        new_img = code_img

        # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        square = drone_data.get("square", False)
        is_barcode = self.drone_data.get("barcode", False)
        # Spacing
        top_padding = drone_data.get("top_padding",(20 - code_img.width//25) + 20)
        if is_barcode: bottom_padding = drone_data.get("bottom_padding", 30)
        else: bottom_padding = drone_data.get("bottom_padding", 0)
        left_padding = drone_data.get("left_padding", top_padding)
        right_padding = drone_data.get("right_padding", 0)
        #Text
        font_path = drone_data.get("font_path", "./assets/font.otf")
        text_margin = drone_data.get("text_margin", 75)
        text_spacing = drone_data.get("text_padding", 0)
        # ID
        text = drone_data.get("drone_id", "")
        id_size = drone_data.get("id_size", None)
        id_shift = drone_data.get("id_shift", 0)
        id_margin = drone_data.get("id_margin_override", text_margin)
        id_spacing = drone_data.get("id_padding_override", text_spacing)
        # Title
        side_text = drone_data.get("title", "")
        title_size = drone_data.get("title_size", None)
        title_shift = drone_data.get("title_shift", 0)
        title_margin = drone_data.get("title_margin_override", text_margin)
        title_spacing = drone_data.get("title_padding_override", text_spacing)

        def __generate_text(text, text_margin, modifier, text_spacing, reqested_size=None):
            # Set Font size
            font_size=1
            if reqested_size == None:
                # Auto Set Font
                font_size = 1
                text_width = 0
                while text_width <= code_img.width - text_margin:
                    font = ImageFont.truetype(font_path, font_size)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    font_size += 1
            else:
                # Set Size from option
                font_size=reqested_size
                font = ImageFont.truetype(font_path, font_size)
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
            text_height = int((bbox[3] - bbox[1])*modifier) + text_spacing
            if any(ord(c) > 127 for c in text): text_height = int(text_height*.75)
            return font, text_height, text_width

        # Render Top Text
        if text != "":
            # Set Font size
            font, id_text_height, id_text_width = __generate_text(text, id_margin, 1.4, id_spacing, id_size)

            # Draw new canvase
            new_img = Image.new("RGB", (code_img.width, code_img.height + id_text_height + bottom_padding + top_padding), back_color)
            draw = ImageDraw.Draw(new_img)

            # Center Text
            text_x = (new_img.width - id_text_width) // 2
            draw.text((text_x+id_shift, top_padding), text, fill=front_color, font=font)

            # Set Image
            new_img.paste(code_img, (0, id_text_height+top_padding))

        # Render Side Text
        if side_text != "":
            # Rotate the image 90 degrees to make it easier to work with
            code_img = new_img.rotate(-90, expand=True)

            # Set Font size
            if is_barcode: title_margin += 20
            font, title_text_height, title_text_width = __generate_text(side_text, title_margin, 1.35, title_spacing, title_size)

            # Draw new canvase
            new_img = Image.new("RGB", (code_img.width, code_img.height + title_text_height + right_padding + left_padding), back_color)
            draw = ImageDraw.Draw(new_img)

            # Center Text
            text_x = ((new_img.width) - title_text_width) // 2
            draw.text((text_x+title_shift, left_padding), side_text, fill=front_color, font=font)

            # Set image and rotate image back to normal
            new_img.paste(code_img, (0, title_text_height+left_padding))
            new_img = new_img.rotate(90, expand=True)

        # Square off image
        if square:
            long_size = max(new_img.width, new_img.height)
            short_size =min(new_img.width, new_img.height)
            squared_img = Image.new("RGB", (long_size, long_size), back_color)
            if new_img.width > new_img.height:
                squared_img.paste(new_img, (0,(long_size - short_size)//2))
            else:
                squared_img.paste(new_img, ((long_size - short_size)//2, 0))
            new_img = squared_img

        self.drone_tag = new_img
        return new_img

    def place_qrcode_logo(self, qr_img, drone_data):

        # Get options
        logo = drone_data.get("logo", None)
        if logo == None:
            return qr_img # if no logo is provided, do nothing.
        else: logo = Image.open(logo)
        logo_mod = drone_data.get("logo_size", 0.2)
        logo_border = drone_data.get("logo_border", 0.2)
        border_radius = drone_data.get("border_radius", 0.125)
        front_color = drone_data.get("logo_color",
        tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        qr_img = qr_img.convert("RGBA")
        logo = logo.convert("RGBA")

        # Recolor logo
        r, g, b, a = logo.split()
        logo = Image.new("RGBA", logo.size, (*front_color, 255))
        logo.putalpha(a)

        # Resize Logo
        qr_w, qr_h = qr_img.size
        logo_size = int(qr_w*logo_mod) # Calcuale logo size
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Add logo border
        pad = int(logo_size*logo_border) # Calcuale border padding
        bg_size = logo_size + pad * 2    # Calcuale border size
        bg = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        # Round conrners
        radius = int(bg_size*border_radius)
        draw.rounded_rectangle(
            (0, 0, bg_size, bg_size),
            radius=radius,
            fill=(*back_color, 255),
        )

        # Center Logo
        bg_x = (qr_w - bg_size) // 2
        bg_y = (qr_h - bg_size) // 2
        logo_x = (qr_w - logo_size) // 2
        logo_y = (qr_h - logo_size) // 2
        qr_img.paste(bg, (bg_x, bg_y), bg)
        qr_img.paste(logo, (logo_x, logo_y), logo)

        return qr_img.convert("RGB")

    def generate_drone_qr(self, drone_data):

        # Imports for this function
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
        from qrcode.image.styles.colormasks import SolidFillColorMask

        # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        qr_roundness = drone_data.get("qr_roundness", 1)
        data = self.drone_data.get("code_data", self.drone_id)

        # QR code generation
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
            module_drawer=RoundedModuleDrawer(radius_ratio=qr_roundness),
            eye_drawer=RoundedModuleDrawer(radius_ratio=qr_roundness),
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=front_color,
            ),
        )

        return qr_img.convert("RGB")

    def generate_drone_barcode(self, drone_data):

        # Imports for this function
        import barcode
        from barcode.writer import ImageWriter

         # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        data = self.drone_data.get("code_data", self.drone_id)
        barcode_height = self.drone_data.get("barcode_height", len(data)+6)

        # Barcode generation
        code128 = barcode.get("Code128", data, writer=ImageWriter())
        img = code128.render(
            {
                "module_width": 0.2,
                "module_height": barcode_height,
                "quiet_zone": 1.8,
                "dpi": 650-(barcode_height*10),
                "write_text": False,
                "foreground": front_color,
                "background": back_color
            }
        )

        return img.convert("RGB")

    def generate_drone_id(self, name, ids=[]):
        # This just does a bunch of stuff to convert a string to a small number.
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

# Call Unit tests
if __name__ == "__main__":
    import Sample as sample
    sample.main()
