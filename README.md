<!-- The packaging cannot display Chinese characters, otherwise the icon will become the default image -->
# pyinstaller .\image_converter_compressor.py --onefile -w -F --distpath .\ --name image_converter_compressor --icon=app.ico
<!-- Version: 1.0.0 -->
# Image Converter Compressor
A simple tool to convert and compress images.
## Features
- Convert images to different formats ("JPEG", "PNG", "GIF", "ICO")
- Compress images to reduce file size (percent)
