from PIL import Image, ImageDraw

image = Image.open("assets/images/health_bar/b0.png")

draw = ImageDraw.Draw(image)

for i in range(1, 100):
    x = i + 48
    draw.line((x, 2, x, 27), fill='green', width=1)

    new_image = image.resize((450, 90))

    new_image.save(f"assets/images/health_bar/b{str(i)}.png")
