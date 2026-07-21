@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo Building Patched OpenComposite (OpenOVR) x64...
echo ===================================================

set "VS_VCVARS="
if exist "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvarsall.bat" (
    set "VS_VCVARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvarsall.bat"
) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" (
    set "VS_VCVARS=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" (
    set "VS_VCVARS=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat"
)

if "%VS_VCVARS%"=="" (
    echo [ERROR] MSVC vcvarsall.bat not found!
    exit /b 1
)

call "%VS_VCVARS%" x64
if errorlevel 1 (
    echo [ERROR] Failed to initialize MSVC x64 environment!
    exit /b 1
)

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

if not exist build (
    mkdir build
)
if not exist build\bin (
    mkdir build\bin
)
cd build

echo Configuring CMake for Release x64 (DX11/DX12 only)...
cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release -DSUPPORT_VK=OFF -DBUILD_WITH_VULKAN_SUPPORT=OFF -DXR_USE_GRAPHICS_API_VULKAN=OFF ..

echo Building OpenComposite DLL binaries...
cmake --build . --config Release
if errorlevel 1 (
    echo [ERROR] CMake build failed!
    exit /b 1
)

echo Building OpenComposite.exe with WinForms resources...
python "%SCRIPT_DIR%compile_exe.py"
if errorlevel 1 (
    echo [ERROR] OpenComposite.exe compilation failed!
    exit /b 1
)

echo ===================================================
echo Build completed successfully!
echo Executable and DLLs are ready in: %CD%\bin
echo ===================================================
endlocal
