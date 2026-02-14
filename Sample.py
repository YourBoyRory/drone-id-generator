from DroneTools import DroneTag
import os, json


#=======================================#
###    EXAMPLE USAGE AND UNIT TEST    ###
#=======================================#

def main():
    drone_ids = [
        os.path.splitext(f)[0]
        for f in os.listdir("./samples")
        if f.lower().endswith(".png")
    ]
    drone_ids = [] # Comment this out to enable loading existing drone name

    drones = [
        # Feat Test
        {
            "name": "Rory",
            "title": "Pup Drone",
            "right_padding": 400,
            "front_color": "#DC141E",
        },
        {
            "drone_id": "U992",
            "barcode": True,
            "font_path": "./assets/font2.otf",
            "title": "Drone",
            "front_color": "#FF8C00",
        },
        {
            "name": "Some Pokemon",
            "title": "Poké Drone",
            "logo": "./assets/rocket.png",
            "front_color": "#DC141E",
            "output_path": "./samples/" # <-- You can add arbitry values to the dict for use in your own code.
        },                              #     These will be ignored and untouched.
        {
            "drone_id": "#0000",
            "title": "Hexcorp",
            "logo": "./assets/hex2.png",
            "logo_size": 0.225,    # <-- Logos usally need tweaking
            "logo_border": 0.133,  # <-- Logos usally need tweaking
            "front_color": "#AB34C7",
        },
        # QR Data
        {
            "name": "Long Website",
            "title": "Somename",
            "code_data": "https://www.example.com/make_this_qr_code_massive_please/make_this_qr_code_EVENMORE_massive_please",
            "front_color": "#FFFF00",
        },
        # real world + hash colision
        {
            "name": "Rory",
            "code_data": "https://www.example.com/",
            "font_path": "./assets/font3.otf",
            "qr_roundness": 0.3,
            "text_padding": -35, # <-- Custom fonts usally need tweaking, See Custom Spacing example bellow
            "top_padding": 40,   # <-- Custom fonts usally need tweaking, See Custom Spacing example bellow
            "back_color": "#b2aa83",
            "front_color": "#4f603b",
        },
        # Bounds testing
        {
            "name": "Long Text",
            "title": "Your Extra Long Text Here",
            "front_color": "#1E90FF",
        },
        {
            "name": "Short Text", # Some words hash the same, such as "Short Text" and "Small Text"
            "title": "s",
            "title_size": 80,     # <-- This may be desired for short text
            "front_color": "#1E90FF",
        },
        {
            "name": "Big Text And Squared",
            "title": "BIG TEXT",
            "title_size": 400,
            "square": True,
            "front_color": "#1E90FF",
        },
        {
            "name": "Small Text", # Some words hash the same, such as "Short Text" and "Small Text"
            "title": "Small",
            "title_size": 30,
            "front_color": "#1E90FF",
        },
        {
            "name": "Custom Spacing",
            "title": "Custom Spacing",
            "text_padding": 150,
            "text_margin": 150,
            "top_padding": -10,
            "bottom_padding": 100,
            "left_padding": 75,
            "right_padding": 100,
            "front_color": "#1E90FF",
        },
        # Stability Test
        {
            "This Will": "Get Skipped"
        },
    ]

    skips = []
    for drone in drones[:]:
        #drone_ids = [] # Uncomment this out to disable collision detection
        test_name = drone.get("name", drone.get("title", drone.get("drone_id", list(drone.values())[0])))
        drone_tag = DroneTag(drone, drone_ids)
        print(f"Test: {test_name} {json.dumps(drone_tag.drone_data, indent=4)}\n")
        if drone_tag.drone_id != None: drone_tag.save(drone.get("output_path", "./samples")+f"/{drone_tag.drone_id}.png")
        else: skips.append(test_name)

    if skips != []:
        print(f"Skipped:")
        for test in skips:
            print(f"    '{test}'")

if __name__ == "__main__":
    main()
