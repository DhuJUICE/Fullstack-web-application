# update_miktex.ps1
Start-Process -FilePath "C:\Program Files\MiKTeX\miktex\bin\x64\miktex-console.exe" `
    -ArgumentList "update", "--non-interactive" `
    -Verb RunAs `
    -WindowStyle Hidden