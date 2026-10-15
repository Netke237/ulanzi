# Ulanzi TC001 Automated Backup & Flash Script (AWTRIX NG)
# Usage: powershell -ExecutionPolicy Bypass -File scripts/flash.ps1

param (
    [string]$ComPort = "",
    [switch]$SkipBackup = $false
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Ulanzi TC001 Automated Flasher (AWTRIX NG)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Step 1: Detect COM Port
if (-not $ComPort) {
    Write-Host "`n[STEP 1] Scanning for connected Ulanzi TC001 (ESP32 USB Serial)..." -ForegroundColor Cyan
    $pnpPort = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object { 
        $_.Class -eq "Ports" -and ($_.FriendlyName -match "CP210|CH340|USB-SERIAL|USB Serial Port") 
    } | Select-Object -First 1

    if ($pnpPort -and ($pnpPort.FriendlyName -match "\((COM\d+)\)")) {
        $ComPort = $Matches[1]
        Write-Host "[OK] Detected Ulanzi on: $ComPort ($($pnpPort.FriendlyName))" -ForegroundColor Green
    } else {
        # Check all available COM ports
        $allPorts = [System.IO.Ports.SerialPort]::GetPortNames()
        if ($allPorts.Count -eq 1) {
            $ComPort = $allPorts[0]
            Write-Host "[OK] Using available port: $ComPort" -ForegroundColor Green
        } else {
            Write-Error "No ESP32 USB Serial device detected. Please ensure the Ulanzi TC001 is connected via USB-C data cable and turned ON."
            Write-Host "Detected COM ports: $($allPorts -join ', ')" -ForegroundColor Yellow
            exit 1
        }
    }
} else {
    Write-Host "[INFO] Using specified COM port: $ComPort" -ForegroundColor Cyan
}

$firmwareBin = "F:\Git\GitHub\Ulanzi\.tools\usb-awtrix-ng\usb-awtrix-ng-4mb.bin"
if (-not (Test-Path $firmwareBin)) {
    Write-Error "Firmware binary not found at $firmwareBin."
    exit 1
}

# Step 2: Backup Stock Firmware
$backupDir = "F:\Git\GitHub\Ulanzi\.tools\backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}
$backupBin = Join-Path $backupDir "tc001-stock-backup.bin"

if (-not $SkipBackup -and -not (Test-Path $backupBin)) {
    Write-Host "`n[STEP 2] Backing up original stock firmware (4 MB)..." -ForegroundColor Cyan
    python -m esptool --chip esp32 --port $ComPort --baud 921600 read_flash 0x0 0x400000 $backupBin
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "High-speed backup failed, retrying at 115200 baud..."
        python -m esptool --chip esp32 --port $ComPort --baud 115200 read_flash 0x0 0x400000 $backupBin
    }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Stock firmware backed up to: $backupBin" -ForegroundColor Green
    } else {
        Write-Warning "Could not complete stock backup. Proceeding to flash..."
    }
} else {
    Write-Host "`n[STEP 2] Skipping stock backup (already exists or flag set)." -ForegroundColor Yellow
}

# Step 3: Flash AWTRIX NG
Write-Host "`n[STEP 3] Flashing AWTRIX NG onto Ulanzi TC001 ($ComPort)..." -ForegroundColor Cyan
python -m esptool --chip esp32 --port $ComPort --baud 460800 write_flash 0x0 $firmwareBin

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Flash at 460800 baud failed, retrying at 115200 baud..."
    python -m esptool --chip esp32 --port $ComPort --baud 115200 write_flash 0x0 $firmwareBin
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "Flashing Completed Successfully!" -ForegroundColor Green
    Write-Host "The Ulanzi TC001 will now reboot with AWTRIX NG." -ForegroundColor Green
    Write-Host "Connect to Wi-Fi hotspot 'AWTRIX-XXXXXX' to set your Wi-Fi credentials." -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Error "Flashing failed with exit code $LASTEXITCODE."
    exit $LASTEXITCODE
}
