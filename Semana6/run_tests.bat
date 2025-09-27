@echo off
echo ============================================
echo Ejecutando tests de Rent a Car (Ficha 3147246)
echo ============================================

REM Instalar dependencias si no están
python -m pip install -r requirements.txt >nul 2>&1

REM Crear carpeta reports si no existe
if not exist reports mkdir reports

echo.
echo ============================================
echo OPCIONES DISPONIBLES
echo ============================================
echo 1. Ejecutar TODOS los tests con cobertura
echo 2. Ejecutar SOLO test_create_alquiler_success
echo 3. Ejecutar SOLO test_update_alquiler
echo 4. Ejecutar SOLO test_delete_alquiler
echo 5. Ejecutar SOLO test_register_rental_user
echo 6. Ejecutar SOLO test_login_rental_user
echo 7. Ejecutar TODOS los tests de autenticacion (test_rental_auth.py)
echo 8. Ejecutar TODOS los tests de CRUD (test_rental.py)
echo ============================================

set /p choice="Selecciona una opcion (1-8): "

if "%choice%"=="1" (
    python -m pytest --cov=routers --cov-report=html:reports/htmlcov > reports\pytest-log.txt
) else if "%choice%"=="2" (
    python -m pytest -v test/test_rental.py::TestRentalAPI::test_create_alquiler_success > reports\pytest-log.txt
) else if "%choice%"=="3" (
    python -m pytest -v test/test_rental.py::TestRentalAPI::test_update_alquiler > reports\pytest-log.txt
) else if "%choice%"=="4" (
    python -m pytest -v test/test_rental.py::TestRentalAPI::test_delete_alquiler > reports\pytest-log.txt
) else if "%choice%"=="5" (
    python -m pytest -v test/test_rental_auth.py::TestRentalAuth::test_register_rental_user > reports\pytest-log.txt
) else if "%choice%"=="6" (
    python -m pytest -v test/test_rental_auth.py::TestRentalAuth::test_login_rental_user > reports\pytest-log.txt
) else if "%choice%"=="7" (
    python -m pytest -v test/test_rental_auth.py > reports\pytest-log.txt
) else if "%choice%"=="8" (
    python -m pytest -v test/test_rental.py > reports\pytest-log.txt
) else (
    echo Opcion invalida.
)

echo.
echo ============================================
echo Proceso finalizado.
echo El log fue guardado en: reports\pytest-log.txt
echo ============================================
pause