import json
import os
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_DATA_PATH = Path(__file__).parent / "data" / "filevine.json"
_db: dict = json.loads(_DATA_PATH.read_text())


def _match(record: dict, field: str, value: str) -> bool:
    """Case-insensitive substring match on a field."""
    return value.lower() in str(record.get(field, "")).lower()


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="filevine-mock",
    version="1.0.0",
    instructions=(
        "Mock Filevine legal case management platform for Habbas & Associates PI firm. "
        "Query matters, clients, tasks, deadlines, case notes, documents, settlement info, "
        "litigation costs, and medical records requests."
    ),
)

# ---------------------------------------------------------------------------
# Matters
# ---------------------------------------------------------------------------

@mcp.tool()
def get_matters(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    status: Optional[str] = Field(default=None, description="Filter by status (partial match), e.g. Active - Litigation | Settled"),
    case_type: Optional[str] = Field(default=None, description="Filter by case type (partial match), e.g. Motor Vehicle Accident | Trucking Accident | Premises Liability"),
    assigned_attorney: Optional[str] = Field(default=None, description="Filter by assigned attorney name (partial match)"),
    client_id: Optional[str] = Field(default=None, description="Filter by client ID, e.g. CL001"),
) -> list[dict]:
    """List matters. Optionally filter by matter ID, status, case type, assigned attorney, or client ID."""
    results = _db["matters"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    if case_type:
        results = [r for r in results if _match(r, "case_type", case_type)]
    if assigned_attorney:
        results = [r for r in results if _match(r, "assigned_attorney", assigned_attorney)]
    if client_id:
        results = [r for r in results if r["client_id"].upper() == client_id.upper()]
    return results


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------

@mcp.tool()
def get_clients(
    client_id: Optional[str] = Field(default=None, description="Filter by client ID, e.g. CL001"),
    last_name: Optional[str] = Field(default=None, description="Filter by last name (partial match)"),
    first_name: Optional[str] = Field(default=None, description="Filter by first name (partial match)"),
) -> list[dict]:
    """List clients. Optionally filter by client ID, last name, or first name."""
    results = _db["clients"]
    if client_id:
        results = [r for r in results if r["client_id"].upper() == client_id.upper()]
    if last_name:
        results = [r for r in results if _match(r, "last_name", last_name)]
    if first_name:
        results = [r for r in results if _match(r, "first_name", first_name)]
    return results


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

@mcp.tool()
def get_tasks(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    assigned_to: Optional[str] = Field(default=None, description="Filter by assignee name (partial match)"),
    status: Optional[str] = Field(default=None, description="Filter by status (partial match), e.g. In Progress | Pending | Not Started | Completed"),
    priority: Optional[str] = Field(default=None, description="Filter by priority (partial match), e.g. Critical | High | Medium"),
) -> list[dict]:
    """List tasks. Optionally filter by matter ID, assignee, status, or priority."""
    results = _db["tasks"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if assigned_to:
        results = [r for r in results if _match(r, "assigned_to", assigned_to)]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    if priority:
        results = [r for r in results if _match(r, "priority", priority)]
    return results


# ---------------------------------------------------------------------------
# Deadlines
# ---------------------------------------------------------------------------

@mcp.tool()
def get_deadlines(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    assigned_to: Optional[str] = Field(default=None, description="Filter by assignee name (partial match)"),
    priority: Optional[str] = Field(default=None, description="Filter by priority (partial match), e.g. Critical | High"),
    type: Optional[str] = Field(default=None, description="Filter by deadline type (partial match), e.g. Discovery | Expert | SOL | Mediation | Deposition | Hearing"),
) -> list[dict]:
    """List deadlines. Optionally filter by matter ID, assignee, priority, or type."""
    results = _db["deadlines"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if assigned_to:
        results = [r for r in results if _match(r, "assigned_to", assigned_to)]
    if priority:
        results = [r for r in results if _match(r, "priority", priority)]
    if type:
        results = [r for r in results if _match(r, "type", type)]
    return results


# ---------------------------------------------------------------------------
# Case Notes
# ---------------------------------------------------------------------------

@mcp.tool()
def get_case_notes(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    created_by: Optional[str] = Field(default=None, description="Filter by author name (partial match)"),
    note_type: Optional[str] = Field(default=None, description="Filter by note type (partial match), e.g. Call | Email | Meeting | Task | Activity"),
) -> list[dict]:
    """List case notes. Optionally filter by matter ID, author, or note type."""
    results = _db["case_notes"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if created_by:
        results = [r for r in results if _match(r, "created_by", created_by)]
    if note_type:
        results = [r for r in results if _match(r, "note_type", note_type)]
    return results


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

@mcp.tool()
def get_documents(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    document_type: Optional[str] = Field(default=None, description="Filter by document type (partial match), e.g. Medical Records | Expert Report | Pleading | Demand Letter"),
    tag: Optional[str] = Field(default=None, description="Filter by tag value (partial match against tags array), e.g. liability | medical | settlement"),
) -> list[dict]:
    """List documents. Optionally filter by matter ID, document type, or tag."""
    results = _db["documents"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if document_type:
        results = [r for r in results if _match(r, "document_type", document_type)]
    if tag:
        results = [
            r for r in results
            if any(tag.lower() in t.lower() for t in r.get("tags", []))
        ]
    return results


# ---------------------------------------------------------------------------
# Settlement Info
# ---------------------------------------------------------------------------

@mcp.tool()
def get_settlement_info(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    current_status: Optional[str] = Field(default=None, description="Filter by current status (partial match), e.g. Pre-Settlement Negotiation | Pre-Demand | Mediation Scheduled | Active Litigation | Settled"),
) -> list[dict]:
    """List settlement info records. Optionally filter by matter ID or current status."""
    results = _db["settlement_info"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if current_status:
        results = [r for r in results if _match(r, "current_status", current_status)]
    return results


# ---------------------------------------------------------------------------
# Litigation Costs
# ---------------------------------------------------------------------------

@mcp.tool()
def get_litigation_costs(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    category: Optional[str] = Field(default=None, description="Filter by category (partial match), e.g. Medical Records | Expert Witness | Court Costs | Investigation | Deposition"),
    status: Optional[str] = Field(default=None, description="Filter by status (partial match), e.g. Paid | Pending"),
) -> list[dict]:
    """List litigation costs. Optionally filter by matter ID, category, or status."""
    results = _db["litigation_costs"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if category:
        results = [r for r in results if _match(r, "category", category)]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    return results


# ---------------------------------------------------------------------------
# Medical Records Requests
# ---------------------------------------------------------------------------

@mcp.tool()
def get_medical_records_requests(
    matter_id: Optional[str] = Field(default=None, description="Filter by matter ID, e.g. MTR01"),
    status: Optional[str] = Field(default=None, description="Filter by status (partial match), e.g. Fulfilled | Pending"),
    provider_type: Optional[str] = Field(default=None, description="Filter by provider type (partial match), e.g. Emergency Room | Specialist | Hospital | Physical Therapy | Rehabilitation"),
) -> list[dict]:
    """List medical records requests. Optionally filter by matter ID, status, or provider type."""
    results = _db["medical_records_requests"]
    if matter_id:
        results = [r for r in results if r["matter_id"].upper() == matter_id.upper()]
    if status:
        results = [r for r in results if _match(r, "status", status)]
    if provider_type:
        results = [r for r in results if _match(r, "provider_type", provider_type)]
    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
