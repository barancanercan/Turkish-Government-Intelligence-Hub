"""
Turkish Government Intelligence Hub - Data Preparation
Veri hazırlama script'i - BU DOSYAYI SADECE 1 KERE ÇALIŞTIR!

Usage:
    python prepare_data.py              # Tüm partileri hazırla
    python prepare_data.py --party CHP  # Sadece CHP'yi hazırla
"""

import argparse
import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, Any

import config
import utils


# ============================================
# HASH HELPERS
# ============================================


def get_file_hash(filepath: Path) -> str:
    """Dosyanın MD5 hash'ini hesaplar."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_hashes() -> Dict[str, str]:
    """Kayıtlı hash'leri yükler."""
    hash_file = config.VECTOR_DB_DIR / "hashes.json"
    if hash_file.exists():
        with open(hash_file, "r") as f:
            return json.load(f)
    return {}


def save_hashes(hashes: Dict[str, str]) -> None:
    """Hash'leri dosyaya kaydeder."""
    config.VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.VECTOR_DB_DIR / "hashes.json", "w") as f:
        json.dump(hashes, f, indent=4)


# ============================================
# MAIN PREPARATION FUNCTION
# ============================================


def prepare_party_data(
    party: str, embeddings: Any = None, force: bool = False
) -> bool:
    """
    Belirli bir partinin PDF verisini işler, metadata ekler ve UNIFIED vektör veritabanına kaydeder.
    Eğer dosya değişmemişse ve force=False ise işlemi atlar.
    """
    pdf_path = config.PARTY_PDFS.get(party)
    if not pdf_path or not pdf_path.exists():
        utils.logger.error(f"❌ {party} için PDF bulunamadı!")
        return False

    # Hash kontrolü
    current_hash = get_file_hash(pdf_path)
    hashes = load_hashes()

    if not force and hashes.get(party) == current_hash and config.UNIFIED_VECTOR_DB.exists():
        utils.logger.info(f"⏩ {party} değişmemiş, atlanıyor.")
        return True

    utils.print_header(f"{party} Veri Hazırlama (Unified)")
    utils.print_party_info(party)

    # 1. PDF kontrolü
    if not utils.validate_pdf_exists(party):
        utils.logger.error(f"❌ {party} için PDF bulunamadı!")
        return False

    # 2. PDF'i yükle
    try:
        pdf_path = config.PARTY_PDFS[party]
        pages = utils.load_pdf(pdf_path)
    except Exception as e:
        utils.logger.error(f"❌ PDF yükleme başarısız: {str(e)}")
        return False

    # 3. Chunk'lara böl ve metadata ekle
    try:
        chunks = utils.chunk_documents(pages)
        for chunk in chunks:
            chunk.metadata["party"] = party  # ← CRITICAL: Metadata filtering için
    except Exception as e:
        utils.logger.error(f"❌ Chunking başarısız: {str(e)}")
        return False

    # 4. Embedding modelini yükle
    if embeddings is None:
        try:
            embeddings = utils.load_embeddings()
        except Exception as e:
            utils.logger.error(f"❌ Embedding model yükleme başarısız: {str(e)}")
            return False

    # 5. Unified Vector DB'ye ekle
    try:
        unified_db_path = config.UNIFIED_VECTOR_DB

        if unified_db_path.exists():
            # Mevcut DB'yi yükle ve yeni dökümanları ekle
            vectorstore = utils.load_vectorstore(unified_db_path, embeddings)

            # Varsa eski partinin verilerini temizle (re-indexing için)
            utils.logger.info(f"🔄 Eski {party} verileri temizleniyor...")
            try:
                # Bazı LangChain/Chroma versiyonlarında bu hata verebiliyor,
                # bu yüzden koruyucu bir blok içine alıyoruz.
                vectorstore.delete(where={"party": party})
            except Exception as e:
                utils.logger.warning(f"⚠️ Eski veriler silinemedi (muhtemelen boş): {str(e)}")

            utils.add_to_vectorstore(chunks, vectorstore)
        else:
            # İlk kez oluştur
            utils.create_vectorstore(chunks, embeddings, unified_db_path)

        utils.logger.info(f"✅ {party} verileri UNIFIED veritabanına eklendi!")

        # Hash'i güncelle
        hashes[party] = current_hash
        save_hashes(hashes)
        return True

    except Exception as e:
        utils.logger.error(f"❌ Veri ekleme başarısız: {str(e)}")
        return False


# ============================================
# BATCH PREPARATION
# ============================================


def prepare_all_parties() -> None:
    """
    Sistem tarafından keşfedilen tüm partilerin verilerini toplu olarak UNIFIED veritabanına hazırlar.
    """
    utils.print_header("🚀 TÜM PARTİLER: UNIFIED VERİ HAZIRLAMA 🚀")

    available_parties = utils.get_available_parties()
    if not available_parties:
        utils.logger.error("❌ Hiç PDF bulunamadı!")
        return

    # Embedding modelini yükle
    try:
        embeddings = utils.load_embeddings()
    except Exception as e:
        utils.logger.error(f"❌ Embedding model yüklenemedi: {str(e)}")
        return

    # Mevcut unified DB'yi temizle (Total Rebuild)
    if config.UNIFIED_VECTOR_DB.exists():
        utils.logger.warning("⚠️ Mevcut UNIFIED veritabanı siliniyor (Total Rebuild)...")
        import shutil

        shutil.rmtree(config.UNIFIED_VECTOR_DB)

    # Her parti için işlem yap (force=True çünkü DB silindi)
    success_count = 0
    for party in available_parties:
        if prepare_party_data(party, embeddings, force=True):
            success_count += 1

    utils.print_header("📊 VERİ HAZIRLAMA ÖZETİ")
    utils.logger.info(f"✅ Başarılı: {success_count}/{len(available_parties)}")
    if success_count == len(available_parties):
        utils.logger.info("🎉 TÜM PARTİLER GÜNCEL!")


# ============================================
# STATUS CHECK
# ============================================


def check_status() -> None:
    """
    Mevcut PDF dosyalarının ve hazırlanan vektör veritabanlarının durumunu ekrana yazdırır.
    """
    utils.print_header("📊 VERİ HAZIRLAMA DURUMU (UNIFIED)")

    all_parties = list(config.PARTY_PDFS.keys())
    available_pdfs = utils.get_available_parties()

    print("\n📁 PDF Durumu:")
    for party in all_parties:
        pdf_status = "✅" if party in available_pdfs else "❌"
        print(f"  {pdf_status} {party}")

    print("\n💾 Unified Database Durumu:")
    db_path = config.UNIFIED_VECTOR_DB
    if db_path.exists():
        print(f"  ✅ Hazır: {db_path}")

        # Koleksiyon içeriğini kontrol et (opsiyonel)
        try:
            embeddings = utils.load_embeddings()
            vectorstore = utils.load_vectorstore(db_path, embeddings)
            count = vectorstore._collection.count()
            print(f"  📦 Toplam Chunk Sayısı: {count}")
        except Exception:
            pass
    else:
        print(f"  ❌ Eksik: {db_path}")

    # Özet
    print("\n📊 Özet:")
    print(f"  📄 Mevcut PDF'ler: {len(available_pdfs)}/{len(all_parties)}")
    if db_path.exists():
        print("  ✅ Sistem kullanıma hazır.")
    else:
        print("  ⚠️ Sistem henüz hazır değil!")


# ============================================
# CLI INTERFACE
# ============================================


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="Turkish Government Intelligence Hub - Veri Hazırlama"
    )

    parser.add_argument(
        "--party",
        type=str,
        choices=list(config.PARTY_PDFS.keys()),
        help="Sadece belirtilen partiyi hazırla",
    )

    parser.add_argument(
        "--status", action="store_true", help="Veri hazırlama durumunu göster"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Mevcut vector DB'yi sil ve yeniden oluştur",
    )

    args = parser.parse_args()

    # Status kontrolü
    if args.status:
        check_status()
        return

    # Tek parti hazırlama
    if args.party:
        success = prepare_party_data(args.party, force=args.force)
        sys.exit(0 if success else 1)

    # Tüm partileri hazırla
    else:
        prepare_all_parties()


# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    main()
