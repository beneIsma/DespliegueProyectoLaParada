# Exporta datos desde SQLite (db.sqlite3) a datos_export.json.
# Requisito: existe db.sqlite3 y el archivo .env NO debe definir DATABASE_URL mientras exportas.
# Uso (PowerShell, desde LPBackend):  .\scripts\export_sqlite_dump.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path "db.sqlite3")) {
    Write-Host "No hay db.sqlite3 en LPBackend. Copia aqui tu SQLite antiguo o omite este paso."
    exit 1
}

$envFile = ".env"
if (-not (Test-Path $envFile)) { Write-Host "Falta .env"; exit 1 }

$backup = ".env.backup_before_sqlite_export"
Copy-Item $envFile $backup -Force

try {
    $lines = Get-Content $envFile
    $filtered = $lines | Where-Object { $_ -notmatch '^\s*DATABASE_URL\s*=' }
    $filtered | Set-Content $envFile -Encoding utf8

    py -3.13 manage.py dumpdata --natural-foreign --natural-primary --indent 2 `
        -e contenttypes -e auth.Permission -e sessions `
        -o datos_export.json
    Write-Host "OK: datos_export.json (restaurando .env)"
}
finally {
    Copy-Item $backup $envFile -Force
    Remove-Item $backup -Force
}
