import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from modules.rag_pipeline import get_rag_pipeline
from modules.database import get_database
from services.whatsapp_service import send_whatsapp
from services.sms_service import send_sms
from services.email_service import send_email


def run_pipeline():
    print("\n" + "=" * 50)
    print("       RAG AGENT CAPSTONE PROJECT")
    print("=" * 50 + "\n")
    
    pipeline = get_rag_pipeline()
    db = get_database()
    
    # Ingest documents
    print("[1] Loading documents...")
    doc_count = pipeline.ingest_documents("./data/sample_documents")
    print(f"    Loaded {doc_count} chunks\n")
    
    # Generate summary
    print("[2] Generating summary...")
    summary = pipeline.generate_summary(
        query="Summarize the main stories and their key characters."
    )
    print(f"    Summary: {summary[:150]}...\n")
    
    # Save to database
    print("[3] Saving to SQLite...")
    summary_id = db.save_summary(summary=summary, query="Story summary")
    print(f"    Saved with ID: {summary_id}\n")
    
    # Send notifications
    print("[4] Sending notifications...")
    
    if settings.TARGET_PHONE_NUMBER:
        result = send_whatsapp(settings.TARGET_PHONE_NUMBER, summary)
        print(f"    WhatsApp: {'Sent' if result['success'] else 'Failed'}")
        
        result = send_sms(settings.TARGET_PHONE_NUMBER, summary)
        print(f"    SMS: {'Sent' if result['success'] else 'Failed'}")
    
    if settings.TARGET_EMAIL:
        result = send_email(settings.TARGET_EMAIL, "RAG Summary", summary)
        print(f"    Email: {'Sent' if result['success'] else 'Failed'}")
    
    print("\n" + "=" * 50)
    print("           COMPLETED")
    print("=" * 50 + "\n")


def test_rag():
    print("\n[TEST MODE]\n")
    
    pipeline = get_rag_pipeline()
    doc_count = pipeline.ingest_documents("./data/sample_documents")
    print(f"Loaded {doc_count} chunks\n")
    
    summary = pipeline.generate_summary()
    print(f"Summary:\n{summary}\n")
    
    db = get_database()
    summary_id = db.save_summary(summary)
    print(f"Saved with ID: {summary_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    
    if args.test:
        test_rag()
    else:
        run_pipeline()
