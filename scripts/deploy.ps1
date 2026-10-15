# Deployment & Verification Script for Ulanzi Home Assistant & Mosquitto on Mini PC (192.168.55.60)
# Usage: powershell -ExecutionPolicy Bypass -File scripts/deploy.ps1

param (
    [string]$TargetHost = "minipc",
    [string]$TargetIp = "192.168.55.60",
    [string]$RemotePath = "C:\GitHub\ulanzi"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Deploying Ulanzi Home Assistant & Mosquitto Stack" -ForegroundColor Cyan
Write-Host "Target: $TargetHost ($TargetIp) -> $RemotePath" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Step 1: Ensure local changes are committed and pushed
Write-Host "`n[STEP 1] Checking git status..." -ForegroundColor Cyan
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Warning "Uncommitted local changes detected. Please commit and push to main before deploying."
}

Write-Host "Pushing latest commits to GitHub origin/main..." -ForegroundColor Cyan
git push origin main 2>$null

# Step 2: Sync or pull repo on Mini PC
Write-Host "`n[STEP 2] Updating repository on Mini PC..." -ForegroundColor Cyan
$updateCommand = @"
powershell -NoProfile -Command "
if (Test-Path '$RemotePath') {
    Set-Location '$RemotePath'
    git pull origin main
} else {
    git clone https://github.com/Netke237/ulanzi.git '$RemotePath'
    Set-Location '$RemotePath'
}
"
"@

ssh $TargetHost $updateCommand
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to update repository on $TargetHost."
    exit $LASTEXITCODE
}

# Step 3: Spin up Docker Compose stack on Mini PC
Write-Host "`n[STEP 3] Starting Docker Compose stack on Mini PC..." -ForegroundColor Cyan
$composeCommand = @"
powershell -NoProfile -Command "
Set-Location '$RemotePath'
docker compose up -d
"
"@

ssh $TargetHost $composeCommand
if ($LASTEXITCODE -ne 0) {
    Write-Error "docker compose up failed on $TargetHost."
    exit $LASTEXITCODE
}

# Step 4: Verify Mosquitto MQTT Broker (port 1883)
Write-Host "`n[STEP 4] Verifying Mosquitto Broker ($TargetIp:1883)..." -ForegroundColor Cyan
$maxRetries = 15
$mqttOk = $false
for ($i = 1; $i -le $maxRetries; $i++) {
    $conn = Test-NetConnection -ComputerName $TargetIp -Port 1883 -WarningAction SilentlyContinue
    if ($conn.TcpTestSucceeded) {
        $mqttOk = $true
        Write-Host "[OK] Mosquitto MQTT broker is listening on port 1883." -ForegroundColor Green
        break
    }
    Start-Sleep -Seconds 2
}
if (-not $mqttOk) {
    Write-Warning "Mosquitto port 1883 not reachable yet. Checking container status..."
}

# Step 5: Verify Home Assistant HTTP interface (port 8123)
Write-Host "`n[STEP 5] Verifying Home Assistant (http://$TargetIp:8123)..." -ForegroundColor Cyan
$haOk = $false
$maxHaRetries = 25
for ($i = 1; $i -le $maxHaRetries; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "http://${TargetIp}:8123" -TimeoutSec 4 -ErrorAction Stop
        if ($resp.StatusCode -eq 200 -or $resp.StatusCode -eq 302) {
            $haOk = $true
            Write-Host "[OK] Home Assistant is reachable on HTTP 8123 (status $($resp.StatusCode))." -ForegroundColor Green
            break
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}
if (-not $haOk) {
    Write-Warning "Home Assistant initial response timed out. Initial container startup can take up to 60 seconds on first run."
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "Deployment Completed!" -ForegroundColor Green
Write-Host "Home Assistant: http://${TargetIp}:8123" -ForegroundColor Green
Write-Host "Mosquitto MQTT: ${TargetIp}:1883" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
