
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
