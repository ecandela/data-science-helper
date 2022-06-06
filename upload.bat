CALL env\Scripts\activate.bat
if exist "dist" rmdir /s dist
py setup.py sdist
twine upload dist/* -u analitica.avanzada -p Windows2020!!!5
PAUSE