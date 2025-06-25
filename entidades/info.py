import re
from typing import Dict, Optional

class Informacao:
    def __init__(self, telefone: Optional[str] = None, endereco: Optional[str] = None, redes_sociais: Optional[str] = None, email: Optional[str] = None) -> None:
        self.telefone = str(telefone) if telefone is not None else ""
        self.endereco = str(endereco) if endereco is not None else ""
        self.redes_sociais = str(redes_sociais) if redes_sociais is not None else ""
        self.email = str(email) if email is not None else ""

    def __str__(self) -> str:
        partes_endereco_str = []
        if self._endereco:
            endereco_principal = f"{self._endereco['rua']}, {self._endereco['numero']}"
            partes_endereco_str.append(endereco_principal)

            if self._endereco['bairro'] and self._endereco['cidade'] and self._endereco['estado']:
                endereco_opcional = (
                    f", {self._endereco['bairro']}, {self._endereco['cidade']}, {self._endereco['estado']}"
                )
                partes_endereco_str.append(endereco_opcional)
        
        endereco_exibicao = "".join(partes_endereco_str) if partes_endereco_str else "N/D"

        return (f"Telefone: {self._telefone}, E-mail: {self._email}, "
                f"Endereço: {endereco_exibicao}, Redes Sociais: {self._redes_sociais if self._redes_sociais else 'N/D'}")

    def __repr__(self) -> str:
        return (f"Informacao(telefone={self._telefone!r}, email={self._email!r}, "
                f"endereco={self._endereco!r}, redes={self._redes_sociais!r})")

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, numero_telefone_str: str) -> None:
        if numero_telefone_str is None or str(numero_telefone_str).strip() == "":
            self._telefone = ""
            return
        try:
            numero_formatado = Informacao.validar_e_formatar_telefone_brasileiro(str(numero_telefone_str))
            if numero_formatado is None:
                raise ValueError("Formato de número de telefone brasileiro inválido.")
            self._telefone = numero_formatado
        except ValueError as e:
            raise e


    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email_str: Optional[str]) -> None:
        try:
            if not email_str or str(email_str).strip().lower() in ["", "none", "null"]:
                self._email = ""
                return

            email_str = str(email_str).strip()
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_str):
                self._email = email_str
            else:
                raise ValueError("Formato de e-mail inválido.")
        except Exception as e:
            print(f"Erro ao validar email '{email_str}': {e}")
            self._email = ""  # fallback defensivo

    @property
    def endereco(self) -> str:
        if not hasattr(self, "_endereco") or not self._endereco:
            return ""

        partes = [self._endereco.get("rua", ""), self._endereco.get("numero", "")]
        
        if "bairro" in self._endereco:
            partes.append(self._endereco["bairro"])
        if "cidade" in self._endereco:
            partes.append(self._endereco["cidade"])
        if "estado" in self._endereco:
            partes.append(self._endereco["estado"])

        return ", ".join(partes)


    @endereco.setter
    def endereco(self, endereco_str: str) -> None:
        if not endereco_str or endereco_str.strip().lower() in ["", "none", "null"]:
            self._endereco = {}
            return

        endereco_str = endereco_str.strip()

        # Substitui hífens por vírgulas se tiver padrão comum
        if "-" in endereco_str and "," in endereco_str:
            endereco_str = endereco_str.replace(" - ", ", ")

        padrao_endereco = re.compile(r"""
            ^\s*
            ([^,]+?)            # Rua
            \s*,\s*
            ([^,]+?)            # Número
            (?:\s*,\s*
                ([^,]+?)        # Bairro
                \s*,\s*
                ([^,]+?)        # Cidade
                \s*,\s*
                ([A-Z]{2})      # Estado
            )?
            \s*$
        """, re.VERBOSE)

        match = padrao_endereco.match(endereco_str)

        if match:
            self._endereco = {
                "rua": match.group(1).strip(),
                "numero": match.group(2).strip()
            }
            if match.group(3): self._endereco["bairro"] = match.group(3).strip()
            if match.group(4): self._endereco["cidade"] = match.group(4).strip()
            if match.group(5): self._endereco["estado"] = match.group(5).strip().upper()
        else:
            raise ValueError("Formato de endereço inválido. Use: 'Rua, Número, Bairro, Cidade, Estado'")

    @property
    def redes_sociais(self) -> str:
        return self._redes_sociais

    @redes_sociais.setter
    def redes_sociais(self, redes_sociais_str: str) -> None:
        self._redes_sociais = str(redes_sociais_str).strip() if redes_sociais_str else ""



    DDDS = {
        "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "21", "22", "24",
        "27", "28",
        "31", "32", "33", "34", "35", "37", "38",
        "41", "42", "43", "44", "45", "46",
        "47", "48", "49",
        "51", "53", "54", "55",
        "61", "62", "63", "64", "65", "66", "67", "68", "69",
        "71", "73", "74", "75", "77", "79",
        "81", "82", "83", "84", "85", "88", "89", "86", "87",
        "91", "92", "93", "94", "95", "96", "97", "98", "99"
    }

    @staticmethod
    def _validar_e_formatar_numero_brasileiro_local(numero_str: str) -> str:
        numero_limpo = re.sub(r'\D', '', numero_str)

        # Lógica para remover prefixo de operadora.
        if len(numero_limpo) == 12 and numero_limpo.startswith('0'):
            numero_limpo = numero_limpo[2:]
        elif len(numero_limpo) == 11 and numero_limpo.startswith('0'):
            numero_limpo = numero_limpo[1:]
    
        if not (len(numero_limpo) == 10 or len(numero_limpo) == 11):
            raise ValueError("Número nacional inválido: Deve ter 10 ou 11 dígitos.")

        ddd = numero_limpo[:2]
        numero_principal = numero_limpo[2:]
    
        if ddd not in Informacao.DDDS:
            raise ValueError(f"Número brasileiro inválido: DDD '{ddd}' não reconhecido.")
        if ddd.startswith('0') or ddd.endswith('0'):
            raise ValueError(f"Número brasileiro inválido: DDD '{ddd}' inválido (não pode começar ou terminar com 0).")

        if numero_principal.startswith('1'):
            raise ValueError("Número brasileiro inválido: Número local não pode começar com 1.")

        if len(numero_principal) == 9: 
            if not numero_principal.startswith(('6', '7', '8', '9')):
                raise ValueError("Número brasileiro inválido: Celular de 9 dígitos deve começar com 6, 7, 8 ou 9.")
            return f"{ddd}{numero_principal[0]}{numero_principal[1:5]}{numero_principal[5:]}"
        elif len(numero_principal) == 8: 
            if numero_principal.startswith(('6', '7', '8', '9')):
                raise ValueError("Número brasileiro inválido: Fixo de 8 dígitos não pode começar com 6, 7, 8 ou 9 (parece celular incompleto).")
            return f"{ddd}{numero_principal[:4]}{numero_principal[4:]}"
        else:
            raise ValueError("Número brasileiro inválido, ocorreu algum erro inesperado.")

    @staticmethod
    def validar_e_formatar_telefone_brasileiro(numero_telefone_str: str) -> Optional[str]:
       padrao_global = re.compile(r"""
           ^
           (?P<ddi_prefix>\+\d{1,3}[\s.]*)? 
           (?P<remaining_number>.*)         
           $
       """, re.VERBOSE)
   
       match = padrao_global.match(numero_telefone_str.strip())
       if not match:
           return None 
   
       ddi_prefixo_capturado = match.group('ddi_prefix')
       numero_restante = match.group('remaining_number').strip()
   
       if not numero_restante:
           return None

       if ddi_prefixo_capturado:
           ddi_limpo = re.sub(r'\D', '', ddi_prefixo_capturado)
           if ddi_limpo == '55':
               return Informacao._validar_e_formatar_numero_brasileiro_local(numero_restante)
           else:
               return f"+{ddi_limpo} {numero_restante}"
       else:
           return Informacao._validar_e_formatar_numero_brasileiro_local(numero_restante)

if __name__ == "__main__":
    pass