@echo off

echo Binary file generation started

if exist build\ (
  echo Deleting build folder ...
  rd /s /q build
)

if exist dist\ (
  echo Deleting dist folder ...
  rd /s /q dist
)

pyinstaller --onefile --name DataEntryWAppNotifier --i favicon.ico src/app.py
copy src\appconfig.json dist
md dist\data