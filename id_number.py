import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

Name="Rory"
color = "#DC141E"


def generate_drone_tag(qr_img, text, front_color, back_color):
    font_size = 81
    font = ImageFont.truetype("./assets/font.otf", font_size)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    padding = 20
    new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
    draw = ImageDraw.Draw(new_img)
    text_x = (new_img.width - text_width) // 2
    draw.text((text_x, 0), text, fill=front_color, font=font)
    new_img.paste(qr_img, (0, text_height + padding))
    return new_img

def generate_drone_qr(drone_id, front_color, back_color):
    qr = qrcode.QRCode(
        version=None,  # auto size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2,
    )
    qr.add_data(drone_id)
    qr.make(fit=True)
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=0.8),
        eye_drawer=SquareModuleDrawer(),  # sharp finder squares
        color_mask=SolidFillColorMask(
            back_color=back_color,        # black background
            front_color=front_color,   # deep red
        ),
    )
    return qr_img.convert("RGB")

def generate_drone_id(name, ids=[]):
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


color = color.lstrip('#')
front_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
back_color = (1, 1, 1)

drone_id = generate_drone_id(Name)
qr = generate_drone_qr(drone_id, front_color, back_color)
final_img = generate_drone_tag(qr, drone_id, front_color, back_color).save(f"{drone_id}.png")

