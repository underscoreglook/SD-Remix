@ECHO OFF

if "%1"=="clean" (
	echo "Cleaning..."
	if EXIST build (
		rmdir /s /q "build"
		mkdir "build"
		echo Clean finished!
	) else (
		echo "Nothing to clean"
	)
	pause
	exit /b 0
)

if [%1]==[] (
	SET target=full
) else (
	SET target=%1
)

echo Build starting for target %target%...
if NOT EXIST build (
	mkdir "build"
)

echo.
echo Extracting Melee ISO...
python.exe scripts\extract_melee_iso.py || exit /b %ERRORLEVEL%

echo.
echo Copying Game Files To Build Folder...
python.exe scripts\copy_game_files.py || exit /b %ERRORLEVEL%

echo.
echo Building system files...
python.exe scripts\build_system_files.py

:: In case we've double clicked on the bat file, keep it around so we can read the output until keyboard input
echo.
echo Build Finished!
pause