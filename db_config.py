"""Database configuration for BHIV Bucket"""
import os
from supabase import create_client, Client

# Mock Supabase config for development
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mock.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "mock_key")

def get_supabase_client() -> Client:
    """Get Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Mock database for development
class MockDB:
    def __init__(self):
        self.reports = []
        self.values_logs = []
    
    def insert_report(self, data):
        report_id = len(self.reports) + 1
        report = {"id": report_id, **data}
        self.reports.append(report)
        return report
    
    def get_report(self, report_id):
        for report in self.reports:
            if report["id"] == report_id:
                return report
        return None
    
    def insert_values_log(self, data):
        log_id = len(self.values_logs) + 1
        log = {"id": log_id, **data}
        self.values_logs.append(log)
        return log

# Global mock database instance
mock_db = MockDB()