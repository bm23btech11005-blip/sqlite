@echo off
echo Setting up Git repository for Ecommerce Data Exercise
echo =====================================================

echo.
echo Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart your command prompt and run this script again
    pause
    exit /b 1
)

echo Git is installed, proceeding with setup...

echo.
echo Step 1: Initialize Git repository
git init

echo.
echo Step 2: Configure Git (if not already configured)
git config --global user.name >nul 2>&1
if %errorlevel% neq 0 (
    set /p username="Enter your Git username: "
    git config --global user.name "%username%"
)

git config --global user.email >nul 2>&1
if %errorlevel% neq 0 (
    set /p email="Enter your Git email: "
    git config --global user.email "%email%"
)

echo.
echo Step 3: Add all files to Git
git add .

echo.
echo Step 4: Create initial commit
git commit -m "Complete ecommerce data exercise with synthetic data generation, SQLite database, and complex SQL analytics"

echo.
echo Step 5: Add remote repository
git remote add origin https://github.com/bm23btech11005-blip/sqlite.git

echo.
echo Step 6: Set default branch to main
git branch -M main

echo.
echo Step 7: Push to repository
git push -u origin main

echo.
echo =====================================================
echo Git setup completed successfully!
echo Your code has been pushed to: https://github.com/bm23btech11005-blip/sqlite.git
echo =====================================================
pause