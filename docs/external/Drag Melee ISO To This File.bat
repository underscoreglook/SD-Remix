@ECHO OFF

echo Applying the patch...
"%~dp0xdelta3.exe" -d -s "%~1" "%~dp0sdr.xdelta" "%~dp0SD_Remix.iso"
echo Patch applied, created "SD_Remix.iso"
pause