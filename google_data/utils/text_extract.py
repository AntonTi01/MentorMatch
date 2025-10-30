from __future__ import annotations

from pathlib import Path
from typing import Optional


                                                    
def _read_text_file(p: Path) -> str:
    """Читает текстовый файл, подбирая подходящую кодировку."""
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return p.read_text(encoding="cp1251", errors="ignore")
        except Exception:
            return ""


                                              
def _read_pdf(p: Path) -> str:
    """Извлекает текст из PDF-документа, объединяя содержимое страниц."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(p))
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join([text for text in parts if text]).strip()
    except Exception:
        return ""


                                               
def _read_docx(p: Path) -> str:
    """Получает текст из документа DOCX построчно."""
    try:
        import docx

        document = docx.Document(str(p))
        parts = []
        for paragraph in document.paragraphs:
            parts.append(paragraph.text or "")
        return "\n".join(parts).strip()
    except Exception:
        return ""


                                                           
def extract_text_from_file(path: Path, mime_type: Optional[str] = None) -> str:
    """Определяет тип файла и извлекает из него текстовое содержимое."""
    if not path or not Path(path).exists():
        return ""
    file_path = Path(path)
    normalized_mime = (mime_type or "").lower()
    extension = file_path.suffix.lower()

    if "pdf" in normalized_mime or extension == ".pdf":
        text = _read_pdf(file_path)
        if text:
            return text
    if "word" in normalized_mime or extension in (".docx",):
        text = _read_docx(file_path)
        if text:
            return text
    return _read_text_file(file_path)
