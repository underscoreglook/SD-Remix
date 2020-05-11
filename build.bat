@ECHO OFF

if EXIST build\root (
	echo Cleaning...
	rmdir /s /q "build\root"
	echo Clean finished
)
mkdir "build\root"
mkdir "build\root\&&SystemData"

echo Copying files...
python.exe scripts\copy_files.py
echo Files copied

echo Building system files...
python.exe scripts\build_system_files.py
echo Finished building system files

echo Remember to build Start.dol using Melee Code Manager
:: In case we've double clicked on the bat file, keep it around so we can read the output until keyboard input
pause