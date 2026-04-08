# Ontology: Организация мероприятий

> Domain ontology per SPF.SPEC.002.

---

## 1. Entity Types

| Code | Type | FPF/SPF Concept | Definition | ≠ (what it is NOT) | Source |
|------|------|-----------------|------------|---------------------|--------|
| M | Method | U.Method | | ≠ scenario, ≠ tool | SPF (base) |
| WP | Work Product | U.Work + U.Episteme | | ≠ method description | SPF (base) |
| FM | Failure Mode | — (SPF-specific) | | ≠ code bug | SPF (base) |
| D | Distinction | A.7 Strict Distinction | | ≠ fact, ≠ definition | SPF (base) |
| R | Role | U.RoleAssignment | | ≠ person, ≠ job title | SPF (base) |
| CHR | Characteristic | U.Characteristic | | ≠ metric | SPF (base) |
| SOTA | SoTA Annotation | — (SPF-specific) | | ≠ literature review | SPF (base) |
| MAP | Map | U.Episteme | | ≠ content | SPF (base) |
| SC | Service Clause | — (SPF-specific) | | ≠ use case | SPF (base) |

---

## 2. Domain Glossary

| Term (RU) | Term (EN) | Definition | Parent Concept (SPF) | Related entity |
|-----------|-----------|-----------|---------------------|----------------|
| | | | | |

---

## 3. Relationships Between Types

| Subject | Relationship | Object | Example |
|---------|-------------|--------|---------|
| Method | produces → | Work Product | |
| Failure Mode | violates ← | Method | |

---

_Ontology per SPF.SPEC.002. Pack ID: OM_
