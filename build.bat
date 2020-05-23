@ECHO OFF

:: If cleaning, just delete and recreate the build directory
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

:: If no target specified, just do a full build
if [%1]==[] (
	SET TARGET=full
) else (
	SET TARGET=%1
)

:: Set up build options based on target
if %TARGET%==full (
    SET buildIso=yes
    SET buildDelta=yes
) ELSE ( IF %TARGET%==iso (
    SET buildIso=yes
    SET buildDelta=no
) ELSE ( IF %TARGET%==xdelta (
    SET buildIso=yes
    SET buildDelta=yes
) ELSE (
    echo "%TARGET%" is not a valid target.
    echo Valid Targets:
    echo - clean:    Cleans the build folder, so next build starts from scratch
    echo - full:     Builds all targets
    echo - iso:      Only builds a playable ISO
    echo - xdelta:   Creates an xdelta patch that can be applied to a Melee ISO to get SD Remix. Also builds the ISO.
    pause
    exit /b 1
)))

:: Proceed with the build
echo Build starting for target %TARGET%...
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
python.exe scripts\build_system_files.py || exit /b %ERRORLEVEL%

if %buildIso%==yes (
    echo.
    echo Building the ISO...
    python.exe scripts\build_iso.py || exit /b %ERRORLEVEL%
)

if %buildDelta%==yes (
    echo.
    echo Creating the patches...
    python.exe scripts\create_patches.py || exit /b %ERRORLEVEL%
)

:: In case we've double clicked on the bat file, keep it around so we can read the output until keyboard input
echo.
if "%2"=="nopause" (
    :: Don't pause
    echo Build Finished!
) else (
    echo Build Finished!
    pause
)