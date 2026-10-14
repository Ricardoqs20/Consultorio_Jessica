"""
Módulo de utilitários de validação e sanitização de dados para o Consultório Art Odonto.
"""

import re
from typing import Dict, Any


class DataValidator:
    """
    Classe responsável por validar entradas cadastrais de pacientes e agendamentos.
    Segue o Princípio de Responsabilidade Única (SRP).
    """

    PHONE_REGEX = r"^\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}$"

    @classmethod
    def validate_phone(cls, phone: str) -> bool:
        """
        Valida números de telefone no formato brasileiro.
        Exemplos válidos: (11) 98765-4321, 11987654321, (21) 3456-7890.
        """
        if not phone:
            return False
        return bool(re.match(cls.PHONE_REGEX, phone.strip()))

    @classmethod
    def sanitize_string(cls, text: str) -> str:
        """Remove espaços excessivos e caracteres perigosos."""
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def validate_appointment(cls, data: Dict[str, Any]) -> bool:
        """Verifica se os campos obrigatórios do agendamento estão presentes e válidos."""
        required = ["nome", "telefone", "servico", "data"]
        for field in required:
            if not data.get(field):
                return False
        return cls.validate_phone(data["telefone"])
