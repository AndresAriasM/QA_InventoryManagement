#!/usr/bin/env python3
"""
Configuración de Seguridad del Sistema de Inventarios
====================================================

Este módulo contiene configuraciones de seguridad centralizadas
para el sistema de gestión de inventarios.
"""

import os
import secrets
import hashlib
from typing import Dict, Any

class ConfiguracionSeguridad:
    """
    Clase para manejar configuraciones de seguridad del sistema.
    """
    
    def __init__(self):
        """Inicializa la configuración de seguridad."""
        self.configuraciones = self._cargar_configuraciones()
    
    def _cargar_configuraciones(self) -> Dict[str, Any]:
        """
        Carga las configuraciones de seguridad desde variables de entorno.
        
        Returns:
            Dict con las configuraciones de seguridad
        """
        return {
            # Configuración de archivos
            'max_file_size': int(os.getenv('MAX_FILE_SIZE', '10485760')),  # 10MB
            'allowed_extensions': os.getenv('ALLOWED_EXTENSIONS', 'json,txt').split(','),
            'upload_folder': os.getenv('UPLOAD_FOLDER', 'uploads'),
            'secure_folder': os.getenv('SECURE_FOLDER', 'secure_data'),
            
            # Configuración de validación
            'max_input_length': int(os.getenv('MAX_INPUT_LENGTH', '1000')),
            'min_password_length': int(os.getenv('MIN_PASSWORD_LENGTH', '8')),
            'session_timeout': int(os.getenv('SESSION_TIMEOUT', '3600')),  # 1 hora
            
            # Configuración de logging
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'inventario.log'),
            'error_log_file': os.getenv('ERROR_LOG_FILE', 'errors.log'),
            'security_log_file': os.getenv('SECURITY_LOG_FILE', 'security.log'),
            
            # Configuración de backup
            'backup_enabled': os.getenv('BACKUP_ENABLED', 'True').lower() == 'true',
            'backup_interval': int(os.getenv('BACKUP_INTERVAL', '86400')),  # 24 horas
            'backup_retention_days': int(os.getenv('BACKUP_RETENTION_DAYS', '30')),
            'backup_folder': os.getenv('BACKUP_FOLDER', 'backups'),
            
            # Configuración de monitoreo
            'monitoring_enabled': os.getenv('MONITORING_ENABLED', 'True').lower() == 'true',
            'alert_email': os.getenv('ALERT_EMAIL', 'admin@empresa.com'),
            'alert_threshold': int(os.getenv('ALERT_THRESHOLD', '5')),
        }
    
    def obtener_clave_segura(self, longitud: int = 32) -> str:
        """
        Genera una clave segura para encriptación.
        
        Args:
            longitud: Longitud de la clave en bytes
            
        Returns:
            str: Clave segura en hexadecimal
        """
        return secrets.token_hex(longitud)
    
    def hash_seguro(self, texto: str, salt: str = None) -> str:
        """
        Genera un hash seguro de un texto.
        
        Args:
            texto: Texto a hashear
            salt: Salt personalizado (opcional)
            
        Returns:
            str: Hash seguro del texto
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combinar texto y salt
        texto_salt = f"{texto}{salt}"
        
        # Generar hash SHA-256
        hash_obj = hashlib.sha256()
        hash_obj.update(texto_salt.encode('utf-8'))
        
        return f"{hash_obj.hexdigest()}:{salt}"
    
    def verificar_hash(self, texto: str, hash_verificar: str) -> bool:
        """
        Verifica si un texto coincide con un hash.
        
        Args:
            texto: Texto a verificar
            hash_verificar: Hash a verificar
            
        Returns:
            bool: True si coincide, False si no
        """
        try:
            hash_original, salt = hash_verificar.split(':')
            hash_calculado = self.hash_seguro(texto, salt)
            hash_calc, _ = hash_calculado.split(':')
            return hash_original == hash_calc
        except ValueError:
            return False
    
    def validar_entrada_segura(self, entrada: str) -> bool:
        """
        Valida que una entrada sea segura.
        
        Args:
            entrada: Entrada a validar
            
        Returns:
            bool: True si es segura, False si no
        """
        if not isinstance(entrada, str):
            return False
        
        # Verificar longitud
        if len(entrada) > self.configuraciones['max_input_length']:
            return False
        
        # Verificar caracteres peligrosos
        caracteres_peligrosos = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`', '$']
        for char in caracteres_peligrosos:
            if char in entrada:
                return False
        
        return True
    
    def sanitizar_entrada(self, entrada: str) -> str:
        """
        Sanitiza una entrada para hacerla segura.
        
        Args:
            entrada: Entrada a sanitizar
            
        Returns:
            str: Entrada sanitizada
        """
        if not isinstance(entrada, str):
            return str(entrada)
        
        # Remover caracteres de control
        entrada_sanitizada = ''.join(char for char in entrada if ord(char) >= 32)
        
        # Limitar longitud
        max_length = self.configuraciones['max_input_length']
        if len(entrada_sanitizada) > max_length:
            entrada_sanitizada = entrada_sanitizada[:max_length]
        
        # Escapar caracteres especiales
        caracteres_especiales = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '&': '&amp;',
        }
        
        for char, escape in caracteres_especiales.items():
            entrada_sanitizada = entrada_sanitizada.replace(char, escape)
        
        return entrada_sanitizada
    
    def obtener_configuracion(self, clave: str, valor_default: Any = None) -> Any:
        """
        Obtiene una configuración específica.
        
        Args:
            clave: Clave de la configuración
            valor_default: Valor por defecto si no existe
            
        Returns:
            Valor de la configuración
        """
        return self.configuraciones.get(clave, valor_default)

# Instancia global de configuración
config_seguridad = ConfiguracionSeguridad()
