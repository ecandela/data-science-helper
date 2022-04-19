CALL env\Scripts\activate.bat
if exist "dist" rmdir /s dist
py setup.py sdist
twine upload dist/*
PAUSE