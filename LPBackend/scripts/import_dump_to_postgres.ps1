# Importa datos_export.json a Postgres (DATABASE_URL en .env debe apuntar a Supabase).
# Uso (PowerShell, desde LPBackend):  .\scripts\import_dump_to_postgres.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path "datos_export.json")) {
    Write-Host "No existe datos_export.json. Ejecuta antes export_sqlite_dump.ps1 con tu SQLite."
    exit 1
}

py -3.13 manage.py loaddata datos_export.json
Write-Host "OK: datos importados."
