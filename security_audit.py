#!/usr/bin/env python3
"""
Script de Auditoría de Seguridad del Sistema de Inventarios
===========================================================

Este script realiza un análisis de seguridad completo del sistema
para identificar vulnerabilidades y problemas de seguridad.
"""

import os
import sys
import json
import re
import ast
import subprocess
from typing import List, Dict, Any, Tuple
from pathlib import Path

class AuditoriaSeguridad:
    """
    Clase para realizar auditorías de seguridad del sistema.
    """
    
    def __init__(self):
        """Inicializa el auditor de seguridad."""
        self.vulnerabilidades = []
        self.recomendaciones = []
        self.archivos_analizados = []
    
    def ejecutar_auditoria_completa(self) -> Dict[str, Any]:
        """
        Ejecuta una auditoría completa de seguridad.
        
        Returns:
            Dict con los resultados de la auditoría
        """
        print("🔍 Iniciando auditoría de seguridad...")
        
        # Analizar archivos Python
        self._analizar_archivos_python()
        
        # Verificar configuraciones
        self._verificar_configuraciones()
        
        # Analizar dependencias
        self._analizar_dependencias()
        
        # Verificar permisos de archivos
        self._verificar_permisos()
        
        # Generar reporte
        reporte = self._generar_reporte()
        
        print("✅ Auditoría completada")
        return reporte
    
    def _analizar_archivos_python(self):
        """Analiza archivos Python en busca de vulnerabilidades."""
        print("📁 Analizando archivos Python...")
        
        archivos_python = list(Path('.').glob('*.py'))
        
        for archivo in archivos_python:
            self.archivos_analizados.append(str(archivo))
            self._analizar_archivo_python(archivo)
    
    def _analizar_archivo_python(self, archivo: Path):
        """Analiza un archivo Python específico."""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar vulnerabilidades comunes
            self._buscar_os_system(archivo, contenido)
            self._buscar_eval_exec(archivo, contenido)
            self._buscar_path_traversal(archivo, contenido)
            self._buscar_hardcoded_secrets(archivo, contenido)
            self._buscar_weak_crypto(archivo, contenido)
            self._buscar_sql_injection(archivo, contenido)
            self._buscar_xss_vulnerabilities(archivo, contenido)
            
        except Exception as e:
            self.vulnerabilidades.append({
                'tipo': 'ERROR_ANALISIS',
                'archivo': str(archivo),
                'severidad': 'MEDIA',
                'descripcion': f'Error al analizar archivo: {e}',
                'linea': 0
            })
    
    def _buscar_os_system(self, archivo: Path, contenido: str):
        """Busca uso inseguro de os.system()."""
        patron = r'os\.system\s*\('
        matches = re.finditer(patron, contenido)
        
        for match in matches:
            self.vulnerabilidades.append({
                'tipo': 'COMMAND_INJECTION',
                'archivo': str(archivo),
                'severidad': 'CRITICA',
                'descripcion': 'Uso inseguro de os.system() - riesgo de inyección de comandos',
                'linea': contenido[:match.start()].count('\n') + 1,
                'codigo': match.group()
            })
    
    def _buscar_eval_exec(self, archivo: Path, contenido: str):
        """Busca uso de eval() o exec()."""
        patrones = [r'eval\s*\(', r'exec\s*\(']
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'CODE_INJECTION',
                    'archivo': str(archivo),
                    'severidad': 'CRITICA',
                    'descripcion': f'Uso de {match.group()} - riesgo de inyección de código',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _buscar_path_traversal(self, archivo: Path, contenido: str):
        """Busca vulnerabilidades de path traversal."""
        patrones = [
            r'open\s*\(\s*[^)]*\.\.',
            r'file\s*\(\s*[^)]*\.\.',
            r'os\.path\.join\s*\([^)]*\.\.'
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'PATH_TRAVERSAL',
                    'archivo': str(archivo),
                    'severidad': 'ALTA',
                    'descripcion': 'Posible vulnerabilidad de path traversal',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _buscar_hardcoded_secrets(self, archivo: Path, contenido: str):
        """Busca secretos hardcodeados."""
        patrones = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'HARDCODED_SECRET',
                    'archivo': str(archivo),
                    'severidad': 'ALTA',
                    'descripcion': 'Posible secreto hardcodeado en el código',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _buscar_weak_crypto(self, archivo: Path, contenido: str):
        """Busca uso de criptografía débil."""
        patrones = [
            r'md5\s*\(',
            r'sha1\s*\(',
            r'DES\s*\(',
            r'RC4\s*\('
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'WEAK_CRYPTO',
                    'archivo': str(archivo),
                    'severidad': 'MEDIA',
                    'descripcion': f'Uso de criptografía débil: {match.group()}',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _buscar_sql_injection(self, archivo: Path, contenido: str):
        """Busca posibles vulnerabilidades de SQL injection."""
        patrones = [
            r'execute\s*\(\s*[^)]*%',
            r'query\s*\(\s*[^)]*\+',
            r'cursor\.execute\s*\(\s*[^)]*%'
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'SQL_INJECTION',
                    'archivo': str(archivo),
                    'severidad': 'ALTA',
                    'descripcion': 'Posible vulnerabilidad de SQL injection',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _buscar_xss_vulnerabilities(self, archivo: Path, contenido: str):
        """Busca vulnerabilidades de XSS."""
        patrones = [
            r'innerHTML\s*=',
            r'document\.write\s*\(',
            r'eval\s*\('
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, contenido)
            for match in matches:
                self.vulnerabilidades.append({
                    'tipo': 'XSS',
                    'archivo': str(archivo),
                    'severidad': 'ALTA',
                    'descripcion': 'Posible vulnerabilidad de XSS',
                    'linea': contenido[:match.start()].count('\n') + 1,
                    'codigo': match.group()
                })
    
    def _verificar_configuraciones(self):
        """Verifica configuraciones de seguridad."""
        print("⚙️ Verificando configuraciones...")
        
        # Verificar archivo .env
        if os.path.exists('.env'):
            self.vulnerabilidades.append({
                'tipo': 'SENSITIVE_FILE',
                'archivo': '.env',
                'severidad': 'ALTA',
                'descripcion': 'Archivo .env presente - verificar que no contenga secretos',
                'linea': 0
            })
        
        # Verificar .gitignore
        if not os.path.exists('.gitignore'):
            self.vulnerabilidades.append({
                'tipo': 'MISSING_GITIGNORE',
                'archivo': '.gitignore',
                'severidad': 'MEDIA',
                'descripcion': 'Archivo .gitignore no encontrado',
                'linea': 0
            })
    
    def _analizar_dependencias(self):
        """Analiza dependencias en busca de vulnerabilidades."""
        print("📦 Analizando dependencias...")
        
        if os.path.exists('requirements.txt'):
            try:
                # Ejecutar safety check
                result = subprocess.run(['safety', 'check'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    self.vulnerabilidades.append({
                        'tipo': 'VULNERABLE_DEPENDENCY',
                        'archivo': 'requirements.txt',
                        'severidad': 'ALTA',
                        'descripcion': 'Dependencias vulnerables encontradas',
                        'linea': 0,
                        'detalles': result.stdout
                    })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
    
    def _verificar_permisos(self):
        """Verifica permisos de archivos."""
        print("🔐 Verificando permisos...")
        
        archivos_sensibles = ['.env', 'config_seguridad.py', '*.log']
        
        for patron in archivos_sensibles:
            for archivo in Path('.').glob(patron):
                if archivo.exists():
                    stat = archivo.stat()
                    permisos = oct(stat.st_mode)[-3:]
                    
                    if permisos in ['666', '777']:
                        self.vulnerabilidades.append({
                            'tipo': 'INSECURE_PERMISSIONS',
                            'archivo': str(archivo),
                            'severidad': 'MEDIA',
                            'descripcion': f'Permisos inseguros: {permisos}',
                            'linea': 0
                        })
    
    def _generar_reporte(self) -> Dict[str, Any]:
        """Genera el reporte final de la auditoría."""
        # Contar vulnerabilidades por severidad
        criticas = len([v for v in self.vulnerabilidades if v['severidad'] == 'CRITICA'])
        altas = len([v for v in self.vulnerabilidades if v['severidad'] == 'ALTA'])
        medias = len([v for v in self.vulnerabilidades if v['severidad'] == 'MEDIA'])
        bajas = len([v for v in self.vulnerabilidades if v['severidad'] == 'BAJA'])
        
        # Generar recomendaciones
        self._generar_recomendaciones()
        
        reporte = {
            'resumen': {
                'total_vulnerabilidades': len(self.vulnerabilidades),
                'criticas': criticas,
                'altas': altas,
                'medias': medias,
                'bajas': bajas,
                'archivos_analizados': len(self.archivos_analizados)
            },
            'vulnerabilidades': self.vulnerabilidades,
            'recomendaciones': self.recomendaciones,
            'archivos_analizados': self.archivos_analizados
        }
        
        return reporte
    
    def _generar_recomendaciones(self):
        """Genera recomendaciones de seguridad."""
        self.recomendaciones = [
            "Implementar validación y sanitización de todas las entradas de usuario",
            "Usar subprocess en lugar de os.system() para ejecutar comandos",
            "Implementar logging de seguridad para monitorear actividades sospechosas",
            "Usar variables de entorno para secretos en lugar de hardcodearlos",
            "Implementar autenticación y autorización si el sistema será multiusuario",
            "Usar HTTPS si el sistema será accesible por red",
            "Implementar backup y recuperación de datos",
            "Realizar auditorías de seguridad regulares",
            "Mantener dependencias actualizadas",
            "Implementar rate limiting para prevenir ataques de fuerza bruta"
        ]
    
    def guardar_reporte(self, archivo: str = 'security_audit_report.json'):
        """Guarda el reporte en un archivo JSON."""
        reporte = self._generar_reporte()
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Reporte guardado en: {archivo}")

def main():
    """Función principal del script de auditoría."""
    print("🔒 Sistema de Auditoría de Seguridad")
    print("=" * 50)
    
    auditor = AuditoriaSeguridad()
    reporte = auditor.ejecutar_auditoria_completa()
    
    # Mostrar resumen
    print("\n📊 RESUMEN DE LA AUDITORÍA:")
    print(f"Total de vulnerabilidades: {reporte['resumen']['total_vulnerabilidades']}")
    print(f"Críticas: {reporte['resumen']['criticas']}")
    print(f"Altas: {reporte['resumen']['altas']}")
    print(f"Medias: {reporte['resumen']['medias']}")
    print(f"Bajas: {reporte['resumen']['bajas']}")
    
    # Guardar reporte
    auditor.guardar_reporte()
    
    # Mostrar vulnerabilidades críticas
    criticas = [v for v in reporte['vulnerabilidades'] if v['severidad'] == 'CRITICA']
    if criticas:
        print("\n🚨 VULNERABILIDADES CRÍTICAS:")
        for vuln in criticas:
            print(f"- {vuln['archivo']}:{vuln['linea']} - {vuln['descripcion']}")

if __name__ == "__main__":
    main()
