"""
test_audit_marketplace.py - Marketplace Validation & Unit Test Suite
Author: Member 3 (Engagement & Validation Suite)
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "audit-orchestrator", "scripts"))
from models import AuditReport, AuditSummary, Finding, SuggestedAction


class TestAuditMarketplace(unittest.TestCase):

    def test_marketplace_manifest(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "..", "marketplace.json")
        self.assertTrue(os.path.exists(manifest_path), "marketplace.json must exist")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertIn("name", data)
        self.assertIn("version", data)
        self.assertIn("entrypoint", data)
        self.assertIn("skills", data)
        self.assertEqual(len(data["skills"]), 4)

    def test_audit_report_schema(self):
        finding = Finding(
            id="F-001",
            title="CSR Text Gap",
            severity="high",
            evidence="Raw text has 50 words.",
            suggested_action=SuggestedAction(summary="Use SSR.", priority="high")
        )
        summary = AuditSummary(total_findings=1, critical=0, high=1, medium=0, low=0)
        report = AuditReport(site="example.com", audited_at="2026-09-01T12:00:00Z", summary=summary, findings=[finding])
        
        report_dict = report.to_dict()
        self.assertEqual(report_dict["site"], "example.com")
        self.assertEqual(report_dict["summary"]["total_findings"], 1)
        self.assertEqual(len(report_dict["findings"]), 1)
        self.assertEqual(report_dict["findings"][0]["id"], "F-001")


if __name__ == "__main__":
    unittest.main()
