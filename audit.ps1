$url = "https://your-project-id.supabase.co" # Replace with your Project URL
$key = "sb_publishable_KTKhi1hZ5-tZ2P3XBVX9Pg_PQWaZ-fI"

Write-Host "--- CYBERVAULT KERNEL: GLOBAL AUDIT ---" -ForegroundColor Cyan
Write-Host "Connecting to Frankfurt Node..." -ForegroundColor Gray

# Pulling the 10% commission data
$headers = @{ "apikey" = "$key"; "Authorization" = "Bearer $key" }
$data = Invoke-RestMethod -Uri "$url/rest/v1/vault_files?select=owner_phone,file_name,price_ugx,maxwell_cut_ugx" -Headers $headers

$totalCut = 0
foreach ($item in $data) {
    Write-Host "Owner: " -NoNewline; Write-Host "$($item.owner_phone)" -ForegroundColor Yellow
    Write-Host "File:  " -NoNewline; Write-Host "$($item.file_name)"
    Write-Host "Cut:   " -NoNewline; Write-Host "UGX $($item.maxwell_cut_ugx)" -ForegroundColor Green
    Write-Host "--------------------------------"
    $totalCut += $item.maxwell_cut_ugx
}

Write-Host "TOTAL COMMISSION EARNED: UGX $totalCut" -ForegroundColor Cyan -BackgroundColor Black
