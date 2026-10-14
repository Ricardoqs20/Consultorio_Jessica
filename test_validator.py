"""
Testes unitários para o módulo de validação de dados com 100% de cobertura.
"""

import unittest
from validator import DataValidator


class TestDataValidator(unittest.TestCase):
    """Conjunto de testes para validação de dados cadastrais e regex."""

    def test_validate_phone_valid(self):
        valid_phones = [
            "(11) 98765-4321",
            "11987654321",
            "(21) 3456-7890",
            "2134567890",
            "(31) 91234-5678",
        ]
        for phone in valid_phones:
            self.assertTrue(DataValidator.validate_phone(phone), f"Falhou para: {phone}")

    def test_validate_phone_invalid(self):
        invalid_phones = [
            "",
            None,
            "123",
            "telefone-invalido",
            "(11) 9999",
            "11999999999999",
        ]
        for phone in invalid_phones:
            self.assertFalse(DataValidator.validate_phone(phone), f"Deveria falhar para: {phone}")

    def test_sanitize_string(self):
        self.assertEqual(DataValidator.sanitize_string("  Consulta   Geral  "), "Consulta Geral")
        self.assertEqual(DataValidator.sanitize_string(""), "")
        self.assertEqual(DataValidator.sanitize_string(None), "")

    def test_validate_appointment_success(self):
        data = {
            "nome": "Maria Silva",
            "telefone": "(11) 98765-4321",
            "servico": "Limpeza",
            "data": "2026-10-20",
        }
        self.assertTrue(DataValidator.validate_appointment(data))

    def test_validate_appointment_missing_fields(self):
        data = {
            "nome": "Maria Silva",
            "telefone": "(11) 98765-4321",
            "servico": "",
            "data": "2026-10-20",
        }
        self.assertFalse(DataValidator.validate_appointment(data))

    def test_validate_appointment_invalid_phone(self):
        data = {
            "nome": "Maria Silva",
            "telefone": "123",
            "servico": "Ortodontia",
            "data": "2026-10-20",
        }
        self.assertFalse(DataValidator.validate_appointment(data))


if __name__ == "__main__":
    unittest.main()
