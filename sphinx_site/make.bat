@echo off
set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%\html
if %errorlevel%==0 (
  echo Build finished. The HTML pages are in %BUILDDIR%\\html
) else (
  echo Sphinx build failed (exit code %errorlevel%)
  exit /b %errorlevel%
)
