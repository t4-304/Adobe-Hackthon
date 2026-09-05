"""
models.py - Core Data Models for Audit Report Schema
Compliant with Adobe University Hackathon 2026 Round 3 Schema Requirements.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SuggestedAction:
    summary: str
    priority: str  # "critical", "high", "medium", "low"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "priority": self.priority
        }


@dataclass
class Finding:
    id: str
    title: str
    severity: str  # "critical", "high", "medium", "low"
    evidence: str
    suggested_action: SuggestedAction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "evidence": self.evidence,
            "suggested_action": self.suggested_action.to_dict()
        }


@dataclass
class AuditSummary:
    total_findings: int
    critical: int
    high: int
    medium: int
    low: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            "total_findings": self.total_findings,
            "critical": self.critical,
            "high": self.high,
            "medium": self.medium
        }


@dataclass
class AuditReport:
    site: str
    audited_at: str
    summary: AuditSummary
    findings: List[Finding]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site": self.site,
            "audited_at": self.audited_at,
            "summary": self.summary.to_dict(),
            "findings": [f.to_dict() for f in self.findings]
        }
