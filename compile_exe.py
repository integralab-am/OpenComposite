import subprocess
import os
import shutil

work_dir = r'c:\wsl\OpenComposite\RuntimeSwitcher'
bin_dir = r'c:\wsl\OpenComposite\build\bin'

os.makedirs(bin_dir, exist_ok=True)

# 1. Copy DLL dependencies and runtime binaries
json_dll_src = r'C:\Users\SERG.DESKTOP-3DD7RP1\.nuget\packages\newtonsoft.json\11.0.2\lib\net45\Newtonsoft.Json.dll'
icon_dll_src = r'C:\Users\SERG.DESKTOP-3DD7RP1\.nuget\packages\osicon\3.0.0\lib\OSIcon.dll'

json_dll = os.path.join(bin_dir, 'Newtonsoft.Json.dll')
icon_dll = os.path.join(bin_dir, 'OSIcon.dll')

shutil.copyfile(json_dll_src, json_dll)
shutil.copyfile(icon_dll_src, icon_dll)

runtime_bin = os.path.join(bin_dir, 'Runtime', 'bin')
os.makedirs(runtime_bin, exist_ok=True)

# Copy compiled vrclient_x64.dll to Runtime\bin and binaries\
binaries_dir = os.path.join(os.path.dirname(bin_dir), 'binaries')
os.makedirs(binaries_dir, exist_ok=True)

compiled_vrclient = os.path.join(bin_dir, 'vrclient_x64.dll')
if os.path.exists(compiled_vrclient):
    try:
        shutil.copyfile(compiled_vrclient, os.path.join(runtime_bin, 'vrclient_x64.dll'))
        shutil.copyfile(compiled_vrclient, os.path.join(binaries_dir, 'vrclient_x64.dll'))
        shutil.copyfile(json_dll_src, os.path.join(runtime_bin, 'Newtonsoft.Json.dll'))
        shutil.copyfile(icon_dll_src, os.path.join(runtime_bin, 'OSIcon.dll'))
    except Exception as e:
        print(f"Notice: file copy skipped: {e}")
    with open(os.path.join(bin_dir, 'Runtime', 'revision.txt'), 'w') as f:
        f.write('bodywalkvr_patched_revision\n')

# 2. Convert .resx to .resources using PowerShell
ps1_path = os.path.join(work_dir, 'convert_res.ps1')
ps1_code = """
Add-Type -AssemblyName System.Windows.Forms
$mw = Join-Path $PSScriptRoot 'MainWindow.resx'
$mwOut = Join-Path $PSScriptRoot 'RuntimeSwitcher.MainWindow.resources'
$r1 = New-Object System.Resources.ResXResourceReader($mw)
$w1 = New-Object System.Resources.ResourceWriter($mwOut)
$n1 = $r1.GetEnumerator()
while ($n1.MoveNext()) { $w1.AddResource($n1.Key, $n1.Value) }
$r1.Close(); $w1.Close()

$ap = Join-Path $PSScriptRoot 'AppListForm.resx'
$apOut = Join-Path $PSScriptRoot 'RuntimeSwitcher.AppListForm.resources'
$r2 = New-Object System.Resources.ResXResourceReader($ap)
$w2 = New-Object System.Resources.ResourceWriter($apOut)
$n2 = $r2.GetEnumerator()
while ($n2.MoveNext()) { $w2.AddResource($n2.Key, $n2.Value) }
$r2.Close(); $w2.Close()
"""
with open(ps1_path, 'w', encoding='utf-8') as f:
    f.write(ps1_code)

res_ps = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps1_path], capture_output=True, text=True)
print("PowerShell ResGen:", res_ps.stdout, res_ps.stderr)

# 3. Compile C# executable using Roslyn csc.exe
csc = r'C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\Roslyn\csc.exe'
out_exe = os.path.join(bin_dir, 'OpenComposite.exe')

res_mw = os.path.join(work_dir, 'RuntimeSwitcher.MainWindow.resources')
res_ap = os.path.join(work_dir, 'RuntimeSwitcher.AppListForm.resources')

cmd = [
    csc, '/target:winexe', f'/out:{out_exe}',
    '/r:System.dll,System.Windows.Forms.dll,System.Drawing.dll,System.Core.dll',
    f'/r:{json_dll}', f'/r:{icon_dll}',
    f'/win32icon:{os.path.join(work_dir, "icon.ico")}',
    f'/res:{res_mw}',
    f'/res:{res_ap}',
    os.path.join(work_dir, '*.cs'),
    os.path.join(work_dir, 'Properties', '*.cs')
]

res_csc = subprocess.run(cmd, capture_output=True, text=True)
print("CSC Returncode:", res_csc.returncode)
print("CSC Output:", res_csc.stdout)
if res_csc.returncode == 0:
    print("SUCCESSFULLY BUILT OpenComposite.exe WITH EMBEDDED WINFORMS RESOURCES!")
