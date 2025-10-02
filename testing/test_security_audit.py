import os
import json     
import pytest
import subprocess   
from pathlib import Path
import sys
# Agregar la raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security_audit import AuditoriaSeguridad, main

# ------------------------------
# FIXTURES
# ------------------------------

@pytest.fixture
def auditor():
    return AuditoriaSeguridad()

@pytest.fixture
def temp_python_file(tmp_path):
    """Crea un archivo Python temporal para pruebas."""
    file_path = tmp_path / "test_vuln.py"
    return file_path

# ------------------------------
# TESTS DE DETECCIÓN DE VULNERABILIDADES
# ------------------------------

def test_detecta_os_system(auditor, temp_python_file):
    temp_python_file.write_text("import os\nos.system('ls')\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'COMMAND_INJECTION' for v in auditor.vulnerabilidades)

def test_detecta_eval_exec(auditor, temp_python_file):
    temp_python_file.write_text("eval('2+2')\nexec('print(123)')\n")
    auditor._analizar_archivo_python(temp_python_file)
    tipos = [v['tipo'] for v in auditor.vulnerabilidades]
    assert "CODE_INJECTION" in tipos

def test_detecta_path_traversal(auditor, temp_python_file):
    temp_python_file.write_text("open('../etc/passwd')\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'PATH_TRAVERSAL' for v in auditor.vulnerabilidades)

def test_detecta_secreto_hardcodeado(auditor, temp_python_file):
    temp_python_file.write_text("password = '1234'\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'HARDCODED_SECRET' for v in auditor.vulnerabilidades)

def test_detecta_criptografia_debil(auditor, temp_python_file):
    temp_python_file.write_text("import hashlib\nhashlib.md5(b'data')\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'WEAK_CRYPTO' for v in auditor.vulnerabilidades)

def test_detecta_sql_injection(auditor, temp_python_file):
    temp_python_file.write_text("cursor.execute('SELECT * FROM users WHERE id=%s' % user_id)\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'SQL_INJECTION' for v in auditor.vulnerabilidades)

def test_detecta_xss(auditor, temp_python_file):
    temp_python_file.write_text("document.write('<script>alert(1)</script>')\n")
    auditor._analizar_archivo_python(temp_python_file)
    assert any(v['tipo'] == 'XSS' for v in auditor.vulnerabilidades)

# ------------------------------
# TESTS DE CONFIGURACIONES
# ------------------------------

def test_verifica_env_file(auditor, tmp_path):
    (tmp_path / ".env").write_text("SECRET=123")
    os.chdir(tmp_path)
    auditor._verificar_configuraciones()
    assert any(v['tipo'] == 'SENSITIVE_FILE' for v in auditor.vulnerabilidades)

def test_verifica_falta_gitignore(auditor, tmp_path):
    os.chdir(tmp_path)
    auditor._verificar_configuraciones()
    assert any(v['tipo'] == 'MISSING_GITIGNORE' for v in auditor.vulnerabilidades)

# ------------------------------
# TESTS DE DEPENDENCIAS
# ------------------------------

def test_analizar_dependencias_vulnerables(monkeypatch, auditor, tmp_path):
    (tmp_path / "requirements.txt").write_text("flask==1.0")
    os.chdir(tmp_path)

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args, returncode=1, stdout="Vulnerable package found")

    monkeypatch.setattr(subprocess, "run", fake_run)
    auditor._analizar_dependencias()
    assert any(v['tipo'] == 'VULNERABLE_DEPENDENCY' for v in auditor.vulnerabilidades)

# ------------------------------
# TESTS DE PERMISOS
# ------------------------------

def test_permisos_inseguros(auditor, tmp_path):
    file = tmp_path / ".env"
    file.write_text("SECRET=123")
    file.chmod(0o666)  # permisos inseguros
    os.chdir(tmp_path)
    auditor._verificar_permisos()
    assert any(v['tipo'] == 'INSECURE_PERMISSIONS' for v in auditor.vulnerabilidades)

# ------------------------------
# TESTS DE REPORTE Y GUARDADO
# ------------------------------

def test_generar_reporte_y_recomendaciones(auditor):
    auditor.vulnerabilidades = [
        {'tipo': 'TEST', 'archivo': 'a.py', 'severidad': 'CRITICA', 'descripcion': 'desc', 'linea': 1}
    ]
    reporte = auditor._generar_reporte()
    assert "resumen" in reporte
    assert "recomendaciones" in reporte
    assert reporte['resumen']['criticas'] == 1

def test_guardar_reporte(auditor, tmp_path):
    file = tmp_path / "reporte.json"
    auditor.vulnerabilidades.append({
        'tipo': 'TEST', 'archivo': 'a.py', 'severidad': 'BAJA', 'descripcion': 'desc', 'linea': 1
    })
    auditor.guardar_reporte(str(file))
    assert file.exists()
    data = json.loads(file.read_text())
    assert "resumen" in data

# ------------------------------
# TEST DE MAIN
# ------------------------------

def test_main(monkeypatch, tmp_path):
    (tmp_path / "dummy.py").write_text("print('hola')\n")
    os.chdir(tmp_path)

    monkeypatch.setattr("builtins.print", lambda *a, **k: None)  # silenciar salida
    main()  # debe ejecutarse sin errores
