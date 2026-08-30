@echo off
echo Installing required packages...
python -m pip install -r requirements.txt

echo.
echo Starting NER Landslide Early Warning dashboard...
streamlit run app.py

pause
