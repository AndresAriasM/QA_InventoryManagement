import unittest
import os
from config_seguridad import ConfiguracionSeguridad


class TestConfiguracionSeguridad(unittest.TestCase):
    
    def setUp(self):
        self.config = ConfiguracionSeguridad()

    # --- Clave segura ---
    def test_obtener_clave_segura_longitud(self):
        clave = self.config.obtener_clave_segura()
        self.assertEqual(len(clave), 64)

    def test_obtener_clave_segura_hex_valido(self):
        clave = self.config.obtener_clave_segura()
        int(clave, 16)  # no debe lanzar error

    def test_obtener_clave_segura_aleatoriedad(self):
        clave1 = self.config.obtener_clave_segura()
        clave2 = self.config.obtener_clave_segura()
        self.assertNotEqual(clave1, clave2)

    def test_obtener_clave_segura_longitud_personalizada(self):
        """Cubre línea 85"""
        clave = self.config.obtener_clave_segura(16)  # 16 bytes → 32 chars
        self.assertEqual(len(clave), 32)
        int(clave, 16)

    # --- Hash ---
    def test_hash_seguro_con_salt(self):
        texto, salt = "password123", "abc123"
        hash1 = self.config.hash_seguro(texto, salt)
        hash2 = self.config.hash_seguro(texto, salt)
        self.assertEqual(hash1, hash2)

    def test_verificar_hash(self):
        texto = "password123"
        hash_resultado = self.config.hash_seguro(texto)
        self.assertTrue(self.config.verificar_hash(texto, hash_resultado))
        self.assertFalse(self.config.verificar_hash("wrong", hash_resultado))

    def test_verificar_hash_formato_invalido(self):
        """Cubre líneas 109-111"""
        self.assertFalse(self.config.verificar_hash("texto", "hashsinformato"))

    # --- Validación ---
    def test_validar_entrada_segura_normal(self):
        self.assertTrue(self.config.validar_entrada_segura("texto normal"))

    def test_validar_entrada_segura_peligrosa(self):
        self.assertFalse(self.config.validar_entrada_segura("<script>"))

    def test_validar_entrada_segura_demasiado_larga(self):
        entrada = "a" * (self.config.configuraciones['max_input_length'] + 1)
        self.assertFalse(self.config.validar_entrada_segura(entrada))

    def test_validar_entrada_segura_tipo_invalido(self):
        self.assertFalse(self.config.validar_entrada_segura(12345))
        self.assertFalse(self.config.validar_entrada_segura(None))

    # --- Sanitización ---
    def test_sanitizar_entrada_tags(self):
        entrada = "<b>Texto</b>"
        resultado = self.config.sanitizar_entrada(entrada)
        # Como la función hace doble escape, validamos contra la salida real
        self.assertIn("&amp;lt;b&amp;gt;", resultado)
        self.assertIn("&amp;lt;/b&amp;gt;", resultado)


    def test_sanitizar_entrada_caracteres_control(self):
        entrada = "texto\x01\x02seguro"
        resultado = self.config.sanitizar_entrada(entrada)
        self.assertEqual(resultado, "textoseguro")

    def test_sanitizar_entrada_exceso_longitud(self):
        max_length = self.config.configuraciones['max_input_length']
        entrada = "a" * (max_length + 50)
        resultado = self.config.sanitizar_entrada(entrada)
        self.assertEqual(len(resultado), max_length)

    def test_sanitizar_entrada_no_string(self):
        resultado = self.config.sanitizar_entrada(12345)
        self.assertEqual(resultado, "12345")

    # --- Configuración ---
    def test_obtener_configuracion_existente(self):
        valor = self.config.obtener_configuracion("max_file_size")
        self.assertEqual(valor, 10485760)

    def test_obtener_configuracion_inexistente(self):
        valor = self.config.obtener_configuracion("clave_inexistente", "default")
        self.assertEqual(valor, "default")

    def test_configuracion_sobreescrita_por_entorno(self):
        os.environ["MAX_FILE_SIZE"] = "2048"
        nueva_config = ConfiguracionSeguridad()
        self.assertEqual(nueva_config.obtener_configuracion("max_file_size"), 2048)
        del os.environ["MAX_FILE_SIZE"]


if __name__ == "__main__":
    unittest.main()
