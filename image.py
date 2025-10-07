from  PIL import  Image
import  os
import glob

thumbnails_images_folder = "thumbnails_image"

def image_compress(filepath):
    print("Hello world")

    validation  = ['.jpeg' ,'.jpg', '.png']
    print(filepath)
    rot,ext = os.path.splitext(filepath)
    print(f"{rot} ,{ext}")
    if ext not in validation:
        print("Invalid format")
    else:
        size = 2 * 1024 * 1024
        file_size = os.path.getsize(filepath)
        print(file_size)
        if file_size < size:
            print(filepath)
        else:
            img = Image.open(filepath)
            print(img)
            #New File
            folder, name = os.path.split(filepath)
            print(f"{folder} and {name}")
            base, ext = os.path.splitext(name)
            print(base)
            print(ext)

            new_file = os.path.join(thumbnails_images_folder, f"{base}_thumbnail{ext}")
            quality = 98
            for i in range(10):
                img.save(new_file, optimize=True, quality=quality)
                print(new_file)
                new_size = os.path.getsize(new_file)
                print(new_size)

                if new_size <= size and quality <= 10:
                    print(f"Image {new_size}")
                    break
                quality -= 5

folder = 'image'
image_ext = ('*.png', '*.jpg', '*.jpeg')
image_path = []
for ext in image_ext:
    image_path.extend(glob.glob(os.path.join(folder,ext)))
print(image_path)



for path in image_path :
    image_compress(path)



