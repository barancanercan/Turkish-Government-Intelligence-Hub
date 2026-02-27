"""
Turkish Government Intelligence Hub - Utility Functions
Yardımcı fonksiyonlar
"""

import logging
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma  # ✅ Yeni paket (deprecation fix)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src import config

# Suppress ChromaDB telemetry
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# ============================================
# LOGGING SETUP
# ============================================

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ============================================
# PDF PROCESSING FUNCTIONS
# ============================================


def load_pdf(pdf_path: Path) -> List[Document]:
    """
    PDF dosyasını yükle

    Args:
        pdf_path: PDF dosya yolu

    Returns:
        List[Document]: Yüklenmiş sayfalar
    """
    try:
        logger.info(f"PDF yükleniyor: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        logger.info(f"✅ {len(pages)} sayfa yüklendi")
        return pages
    except FileNotFoundError:
        logger.error(f"❌ PDF bulunamadı: {pdf_path}")
        raise
    except Exception as e:
        logger.error(f"❌ PDF yükleme hatası: {str(e)}")
        raise


def chunk_documents(
    pages: List[Document],
    chunk_size: int = config.CHUNK_SIZE,
    chunk_overlap: int = config.CHUNK_OVERLAP,
) -> List[Document]:
    """
    Dökümanları chunk'lara böl

    Args:
        pages: PDF sayfaları
        chunk_size: Chunk boyutu
        chunk_overlap: Chunk overlap

    Returns:
        List[Document]: Chunk'lanmış dökümanlar
    """
    logger.info(
        f"Metin chunk'lara bölünüyor (size={chunk_size}, overlap={chunk_overlap})..."
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    chunks = text_splitter.split_documents(pages)
    logger.info(f"✅ {len(chunks)} chunk oluşturuldu")

    return chunks


# ============================================
# EMBEDDING FUNCTIONS
# ============================================


def load_embeddings(model_name: str = config.EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    """
    Türkçe embedding modelini yükle

    Args:
        model_name: HuggingFace model adı

    Returns:
        HuggingFaceEmbeddings: Yüklenmiş embedding modeli
    """
    logger.info(f"Embedding modeli yükleniyor: {model_name}")

    try:
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        logger.info("✅ Embedding modeli hazır")
        return embeddings
    except Exception as e:
        logger.error(f"❌ Embedding yükleme hatası: {str(e)}")
        raise


# ============================================
# VECTOR DATABASE FUNCTIONS
# ============================================


def create_vectorstore(
    chunks: List[Document],
    embeddings: HuggingFaceEmbeddings,
    persist_dir: Path,
    collection_name: str = config.COLLECTION_NAME,
) -> Chroma:
    """
    Vector database oluştur ve kaydet.

    Args:
        chunks: Chunk'lanmış dökümanlar.
        embeddings: Embedding modeli.
        persist_dir: Kaydedilecek dizin.
        collection_name: Koleksiyon adı.

    Returns:
        Chroma: Oluşturulan vector database.
    """
    logger.info(
        f"Vector database oluşturuluyor: {persist_dir} (Collection: {collection_name})"
    )

    try:
        persist_dir.mkdir(parents=True, exist_ok=True)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(persist_dir),
            collection_name=collection_name,
        )

        logger.info(f"✅ Vector database kaydedildi: {persist_dir}")
        return vectorstore

    except Exception as e:
        logger.error(f"❌ Vector DB oluşturma hatası: {str(e)}")
        raise


def add_to_vectorstore(
    chunks: List[Document],
    vectorstore: Chroma,
) -> None:
    """
    Mevcut bir vector database'e yeni dökümanlar ekler.

    Args:
        chunks: Eklenecek chunk'lanmış dökümanlar.
        vectorstore: Hedef vector database.
    """
    logger.info(f"Vector database'e {len(chunks)} yeni chunk ekleniyor...")
    try:
        vectorstore.add_documents(chunks)
        logger.info("✅ Dökümanlar başarıyla eklendi.")
    except Exception as e:
        logger.error(f"❌ Döküman ekleme hatası: {str(e)}")
        raise


def load_vectorstore(
    persist_dir: Path,
    embeddings: HuggingFaceEmbeddings,
    collection_name: str = config.COLLECTION_NAME,
) -> Chroma:
    """
    Hazır vector database'i yükle.

    Args:
        persist_dir: Vector DB dizini.
        embeddings: Embedding modeli.
        collection_name: Koleksiyon adı.

    Returns:
        Chroma: Yüklenmiş vector database.
    """
    logger.info(
        f"Vector database yükleniyor: {persist_dir} (Collection: {collection_name})"
    )

    try:
        if not persist_dir.exists():
            raise FileNotFoundError(f"Vector DB bulunamadı: {persist_dir}")

        vectorstore = Chroma(
            persist_directory=str(persist_dir),
            embedding_function=embeddings,
            collection_name=collection_name,
        )

        logger.info("✅ Vector database yüklendi")
        return vectorstore

    except Exception as e:
        logger.error(f"❌ Vector DB yükleme hatası: {str(e)}")
        raise


# ============================================
# SEARCH FUNCTIONS
# ============================================


def search_similar_docs(
    vectorstore: Chroma,
    question: str,
    top_k: int = config.TOP_K,
    filter_metadata: Optional[Dict[str, Any]] = None,
) -> Tuple[str, List[float], List[Document]]:
    """
    Benzer dökümanları bul (opsiyonel metadata filtresi ile).

    Args:
        vectorstore: Vector database.
        question: Kullanıcı sorusu.
        top_k: Kaç chunk getirileceği.
        filter_metadata: Metadata filtresi (Örn: {"party": "CHP"}).

    Returns:
        Tuple[str, List[float], List[Document]]: (Birleştirilmiş metin, Benzerlik skorları, Orjinal dökümanlar).
    """
    logger.info(f"Arama yapılıyor: '{question}' (Filtre: {filter_metadata})")

    try:
        relevant_docs_with_scores = vectorstore.similarity_search_with_score(
            question, k=top_k, filter=filter_metadata
        )

        if not relevant_docs_with_scores:
            return "", [], []

        relevant_docs = [doc for doc, score in relevant_docs_with_scores]
        relevant_chunks = [doc.page_content for doc in relevant_docs]
        context = "\n\n".join(relevant_chunks)
        scores = [score for doc, score in relevant_docs_with_scores]

        logger.info(f"✅ {len(relevant_docs)} chunk bulundu, skorlar: {scores}")

        return context, scores, relevant_docs

    except Exception as e:
        logger.error(f"❌ Arama hatası: {str(e)}")
        raise


# ============================================
# VALIDATION FUNCTIONS
# ============================================


def validate_pdf_exists(party: str) -> bool:
    """
    Parti PDF'inin var olup olmadığını kontrol et

    Args:
        party: Parti kısa adı (CHP, AKP, etc.)

    Returns:
        bool: PDF var mı?
    """
    pdf_path = config.PARTY_PDFS.get(party)

    if pdf_path is None:
        logger.error(f"❌ Parti bulunamadı: {party}")
        return False

    if not pdf_path.exists():
        logger.warning(f"⚠️ PDF bulunamadı: {pdf_path}")
        return False

    return True


def get_available_parties() -> List[str]:
    """
    Mevcut PDF'leri olan partileri listele

    Returns:
        List[str]: Mevcut partiler
    """
    available = []

    for party, pdf_path in config.PARTY_PDFS.items():
        if pdf_path.exists():
            available.append(party)

    return available


def get_prepared_parties() -> List[str]:
    """
    Unified Vector DB'si hazır olan veya verisi bulunan partileri listeler.

    Returns:
        List[str]: Hazır olan partilerin listesi.
    """
    if config.UNIFIED_VECTOR_DB.exists():
        # Eğer unified DB varsa, PDF'i olan tüm partilerin hazır olduğunu varsayıyoruz.
        # Daha kesin çözüm için DB içindeki metadata'ları sorgulamak gerekebilir.
        return get_available_parties()

    return []


# ============================================
# DISPLAY FUNCTIONS
# ============================================


def print_header(text: str, width: int = 60):
    """Başlık yazdır"""
    import sys
    safe_text = text.encode('ascii', errors='replace').decode('ascii')
    print("\n" + "=" * width, file=sys.stderr)
    print(safe_text.center(width), file=sys.stderr)
    print("=" * width, file=sys.stderr)


def print_party_info(party: str):
    """Parti bilgilerini yazdır"""
    import sys
    info = config.PARTY_INFO.get(party)
    if info:
        print(f"\n{info.get('hex_color', '#0066FF')} {info['name']} ({info['short']})", file=sys.stderr)
        print(f"Website: {info['website']}", file=sys.stderr)


# ============================================
# DYNAMIC PARTY DISCOVERY
# ============================================


def discover_parties() -> Dict[str, Path]:
    """
    data/ klasöründeki tüm PDF'leri otomatik keşfeder.

    Örnek:
        chp.pdf → CHP
        dem.pdf → DEM
        iyip.pdf → IYIP

    Returns:
        Dict[str, Path]: Parti adı (anahtar) ve PDF dosya yolu (değer) sözlüğü.
    """
    pdf_dir = config.DATA_DIR
    parties = {}

    if not pdf_dir.exists():
        logger.warning(f"⚠️ Data klasörü bulunamadı: {pdf_dir}")
        return parties

    for pdf_file in pdf_dir.glob("*.pdf"):
        party_name = pdf_file.stem.upper()  # chp.pdf → CHP
        parties[party_name] = pdf_file
        logger.info(f"✅ Keşfedilen parti: {party_name}")

    if not parties:
        logger.warning("⚠️ Hiç PDF bulunamadı!")
        return {}

    logger.info(f"✅ Toplam {len(parties)} parti keşfedildi")
    return parties


def get_or_create_vectorstore(party: str, embeddings: HuggingFaceEmbeddings) -> Chroma:
    """
    Parti için vector database'i yükle veya oluştur

    - Eğer DB varsa: yükle (fast, ~2s)
    - Eğer DB yoksa: otomatik oluştur (one-time, ~3-5 min)

    Args:
        party: Parti adı (CHP, AKP, DEM, vb.)
        embeddings: Embedding modeli

    Returns:
        Chroma: Vector database

    Raises:
        FileNotFoundError: PDF bulunamadı
    """
    db_path = config.VECTOR_DB_DIR / f"{party.lower()}_db"
    pdf_path = config.DATA_DIR / f"{party.lower()}.pdf"

    # ✅ DB zaten varsa, yükle (fast)
    if db_path.exists():
        logger.info(f"✅ {party} verileri cache'den yükleniyor...")
        return load_vectorstore(db_path, embeddings)

    # ❌ DB yoksa ve PDF varsa, otomatik oluştur
    if not pdf_path.exists():
        error_msg = f"❌ PDF bulunamadı: {pdf_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    logger.info(f"🔄 {party} için veri hazırlanıyor (ilk kez, ~3-5 min)...")

    try:
        # Pipeline: PDF → Chunks → Embeddings → Vector DB
        logger.info(f"  1️⃣ PDF yükleniyor: {party}")
        pages = load_pdf(pdf_path)

        logger.info("  2️⃣ Chunk'lara bölünüyor...")
        chunks = chunk_documents(pages)

        logger.info("  3️⃣ Vector DB oluşturuluyor...")
        vectorstore = create_vectorstore(chunks, embeddings, db_path)

        logger.info(f"✅ {party} hazırlama tamamlandı!")
        return vectorstore

    except Exception as e:
        logger.error(f"❌ {party} hazırlama hatası: {str(e)}")
        raise
