Write-Host "Running tests..."

if (Test-Path "reports") {
    Remove-Item reports\* -Recurse -Force
} else {
    New-Item -ItemType Directory -Path reports | Out-Null
}

pytest --alluredir=reports/

allure generate reports/ -o allure-report --clean

allure open allure-report