from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def adjust_color_for_display(hex_code, display_type):
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    if display_type == "OLED":
        pass
    elif display_type == "LCD":
        r = min(255, int(r * 1.1))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
    elif display_type == "MicroLED":
        pass
    elif display_type == "EInk":
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        r, g, b = gray, gray, gray
    elif display_type == "LTPO":
        pass
    elif display_type == "Foldable":
        r = min(255, int(r * 1.05))
        g = min(255, int(g * 1.05))
        b = min(255, int(b * 1.05))
    else:
        raise ValueError("Invalid display type.")

    adjusted_hex = f"{r:02X}{g:02X}{b:02X}"
    return adjusted_hex


def simulate_color_blindness(hex_code, color_blindness_type):
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    rgb = np.array([r / 255.0, g / 255.0, b / 255.0])

    if color_blindness_type == "Protanopia":
        transformation_matrix = np.array([
            [0.56667, 0.43333, 0.00000],
            [0.55833, 0.44167, 0.00000],
            [0.00000, 0.24167, 0.75833]
        ])
    elif color_blindness_type == "Deuteranopia":
        transformation_matrix = np.array([
            [0.62500, 0.37500, 0.00000],
            [0.70000, 0.30000, 0.00000],
            [0.00000, 0.30000, 0.70000]
        ])
    elif color_blindness_type == "Tritanopia":
        transformation_matrix = np.array([
            [0.95000, 0.05000, 0.00000],
            [0.00000, 0.43333, 0.56667],
            [0.00000, 0.47500, 0.52500]
        ])
    else:
        raise ValueError("Invalid color blindness type.")

    simulated_rgb = np.dot(transformation_matrix, rgb)
    simulated_rgb = np.clip(simulated_rgb, 0, 1) * 255
    r_sim, g_sim, b_sim = map(int, simulated_rgb)
    simulated_hex = f"{r_sim:02X}{g_sim:02X}{b_sim:02X}"
    return simulated_hex


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        hex_code = request.form.get("hex_code").strip().upper()
        if len(hex_code) == 6 and all(c in "0123456789ABCDEF" for c in hex_code):
            # Adjust colors for different displays
            display_types = ["OLED", "LCD", "MicroLED", "EInk", "LTPO", "Foldable"]
            for display in display_types:
                adjusted_color = adjust_color_for_display(hex_code, display)
                results.append((f"Adjusted for {display}", adjusted_color))

            # Simulate colors for color blindness
            color_blindness_types = ["Protanopia", "Deuteranopia", "Tritanopia"]
            for cb_type in color_blindness_types:
                simulated_color = simulate_color_blindness(hex_code, cb_type)
                results.append((f"Simulated for {cb_type}", simulated_color))
        else:
            results.append(("Error", "Invalid color code!"))
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)