import os
import subprocess
import urllib.request
from pathlib import Path

# Получаем корпоративный прокси
proxy_url = urllib.request.getproxies()["https"]

# Файл для сохранения
output_file = Path.cwd() / "cbr_test.xml"

# PowerShell-скрипт
ps_script = r"""
$ErrorActionPreference = "Stop";

$proxy = [System.Net.WebProxy]::new($env:CBR_PROXY);

$proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials;

$client = [System.Net.WebClient]::new();

$client.Proxy = $proxy;

$client.DownloadFile(
    "https://www.cbr.ru/scripts/XML_daily.asp",
    $env:CBR_OUTPUT
);

Write-Output "OK";
"""

# Передаём параметры
env = os.environ.copy()

env["CBR_PROXY"] = proxy_url
env["CBR_OUTPUT"] = str(output_file)

# Запускаем PowerShell
result = subprocess.run(
    [
        "powershell.exe",
        "-NoProfile",
        "-Command",
        ps_script
    ],
    capture_output=True,
    text=True,
    env=env,
    timeout=45
)

print("Код завершения:", result.returncode)
print("Результат:", result.stdout)
print("Ошибка:", result.stderr)

if result.returncode == 0 and output_file.exists():
    print("XML успешно загружен!")
    print("Путь:", output_file)
