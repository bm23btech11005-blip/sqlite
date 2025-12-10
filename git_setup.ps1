# PowerShell script to setup Git repository for Ecommerce Data Exercise
Write-Host "Setting up Git repository for Ecommerce Data Exercise" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and run this script again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Initialize Git repository" -ForegroundColor Cyan
git init

Write-Host ""
Write-Host "Step 2: Configure Git (if needed)" -ForegroundColor Cyan
try {
    $userName = git config --global user.name
    if (-not $userName) {
        $userName = Read-Host "Enter your Git username"
        git config --global user.name $userName
    }
    
    $userEmail = git config --global user.email
    if (-not $userEmail) {
        $userEmail = Read-Host "Enter your Git email"
        git config --global user.email $userEmail
    }
} catch {
    Write-Host "Git configuration may need to be set manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Add all files to Git" -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Step 4: Create initial commit" -ForegroundColor Cyan
git commit -m "Complete ecommerce data exercise with synthetic data generation, SQLite database, and complex SQL analytics"

Write-Host ""
Write-Host "Step 5: Add remote repository" -ForegroundColor Cyan
git remote add origin https://github.com/bm23btech11005-blip/sqlite.git

Write-Host ""
Write-Host "Step 6: Set default branch to main" -ForegroundColor Cyan
git branch -M main

Write-Host ""
Write-Host "Step 7: Push to repository" -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Git setup completed successfully!" -ForegroundColor Green
Write-Host "Your code has been pushed to: https://github.com/bm23btech11005-blip/sqlite.git" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

Read-Host "Press Enter to exit"