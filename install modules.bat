@echo off
echo INSTALLATION WILL BEGIN

:start
cls

:: Ensure the script runs from the directory it's located in
cd /d "%~dp0"

:: Print the current directory for verification
echo Current directory is: %cd%

:: Install Python packages
cd \
cd \python%python_ver%\Scripts\
pip install tk
pip install ruamel.yaml
pip install pillow
pip install qrcode


:: Define the source and intermediate directories
set "source_font_dir=%cd%\POS-tkinter-GUI\Assets\Montserrat static fonts"
set "intermediate_dir=%cd%\POS-tkinter-GUI\Assets\Montserrat static fonts"
set "target_font_dir=C:\Windows\Fonts"

:: Install TTF fonts
echo Installing fonts from "%intermediate_dir%" to "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Black.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-BlackItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Bold.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-BoldItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-ExtraBold.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-ExtraBoldItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-ExtraLight.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-ExtraLightItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Italic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Light.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-LightItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Medium.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-MediumItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Regular.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-SemiBold.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-SemiBoldItalic.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-Thin.ttf" "%target_font_dir%"
xcopy /Y "%intermediate_dir%\Montserrat-ThinItalic.ttf" "%target_font_dir%"

echo INSTALLATION COMPLETE!
pause
exit