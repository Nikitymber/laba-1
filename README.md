import os
import subprocess
import urllib.request
from pathlib import Path

# Получаем адрес корпоративного прокси
proxy_url = urllib.request.getproxies()["https"]

# Куда сохранить XML
output_file = Path.cwd() / "cbr_test.xml"

ps_script = r"""
$ErrorActionPreference = "Stop"

$proxy = New-Object System.Net.WebProxy($env:CBR_PROXY)
$proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials

$client = New-Object System.Net.WebClient
$client.Proxy = $proxy

$client.DownloadFile(
    "https://www.cbr.ru/scripts/XML_daily.asp",
    $env:CBR_OUTPUT
)

Write-Output "OK"
"""

env = os.environ.copy()
env["CBR_PROXY"] = proxy_url
env["CBR_OUTPUT"] = str(output_file)

result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-Command", ps_script],
    capture_output=True,
    text=True,
    env=env,
    timeout=45
)

print("Код завершения:", result.returncode)
print("Результат:", result.stdout)
print("Ошибка:", result.stderr)

if result.returncode == 0:
    print("Файл сохранён:", output_file)
