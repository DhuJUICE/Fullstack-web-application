# schedule_update.ps1
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File .\update_miktex.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "2:00AM"  # Adjust as needed
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Specify the administrator account to avoid permission issues
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount

# Register the task
try {
    Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal -TaskName "UpdateMiKTeX" -Description "Daily MiKTeX update"
    Write-Host "Scheduled task created successfully."
} catch {
    Write-Host "Error creating scheduled task: $_"
}
