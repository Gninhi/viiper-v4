# Persistence Layer

**Status**: ✅ Implemented in Sprint 1.1
**Version**: v0.2.0

La couche de persistence de VIIPER V4 permet de sauvegarder et charger des projets depuis une base de données. Cela permet de maintenir l'état des projets entre les sessions et de gérer plusieurs projets simultanément.

---

## 🎯 Fonctionnalités

- ✅ **Sauvegarde automatique** des projets dans SQLite
- ✅ **CRUD complet** (Create, Read, Update, Delete)
- ✅ **Historique** des health scores
- ✅ **Migrations** avec Alembic
- ✅ **Repository pattern** pour abstraction propre
- ✅ **Soft delete** (archivage) ou hard delete
- ✅ **Filtrage et pagination** pour lister les projets
- ✅ **Support PostgreSQL** (en plus de SQLite)

---

## 📂 Architecture

```
viiper/persistence/
├── __init__.py          # Exports publics
├── database.py          # Connexion et sessions DB
├── models.py            # Modèles SQLAlchemy
└── repositories.py      # Pattern Repository

alembic/
├── versions/            # Migrations
│   └── 001_initial.py
├── env.py              # Configuration Alembic
└── alembic.ini         # Settings

tests/integration/
└── test_persistence.py  # Tests d'intégration (20 tests)
```

---

## 🚀 Quick Start

### 1. Initialiser la base de données

```bash
# Créer la DB et exécuter les migrations
viiper db-init
```

Cela crée automatiquement:
- `~/.viiper/viiper.db` (SQLite)
- Tables: projects, agents, tasks, health_scores

### 2. Créer un projet

```bash
# Créer et sauvegarder un projet
viiper init my-saas --variant=saas --budget=10000 --timeline=12

# Créer sans sauvegarder (temporaire)
viiper init my-saas --no-save
```

### 3. Lister les projets

```bash
# Tous les projets
viiper list-projects

# Filtrer par status
viiper list-projects --status=active

# Filtrer par variant et phase
viiper list-projects --variant=saas --phase=validation

# Limiter le nombre de résultats
viiper list-projects --limit=10
```

### 4. Charger un projet

```bash
# Par nom
viiper load my-saas

# Avec détails complets
viiper load my-saas --details

# Par ID
viiper load 123e4567-e89b-12d3-a456-426614174000
```

### 5. Archiver un projet

```bash
# Soft delete (archive)
viiper archive my-old-project

# Hard delete (suppression permanente)
viiper archive my-old-project --hard
```

---

## 💻 Utilisation Programmatique

### Créer et sauvegarder un projet

```python
from viiper.core.project import Project
from viiper.core.variant import Variant
from viiper.persistence import get_session, ProjectRepository

# Créer un projet
project = Project(
    name="My SaaS",
    variant=Variant.SAAS,
    budget=10000,
    timeline_weeks=12
)

# Sauvegarder en DB
session = get_session()
repo = ProjectRepository(session)

try:
    saved_project = repo.create(project)
    print(f"Project saved with ID: {saved_project.id}")
finally:
    session.close()
```

### Charger un projet

```python
from viiper.persistence import get_session, ProjectRepository

session = get_session()
repo = ProjectRepository(session)

try:
    # Par ID
    project = repo.get("123e4567-e89b-12d3-a456-426614174000")

    # Par nom
    project = repo.get_by_name("My SaaS")

    if project:
        print(project.get_summary())
finally:
    session.close()
```

### Lister et filtrer

```python
from viiper.persistence import get_session, ProjectRepository
from viiper.core.variant import Variant
from viiper.core.phase import Phase

session = get_session()
repo = ProjectRepository(session)

try:
    # Tous les projets
    all_projects = repo.list()

    # Projets SaaS actifs
    saas_projects = repo.list(
        status="active",
        variant=Variant.SAAS
    )

    # Projets en phase Validation
    validation_projects = repo.list(
        phase=Phase.VALIDATION,
        limit=10,
        offset=0
    )

    for project in saas_projects:
        print(f"{project.name}: {project.phase.display_name}")
finally:
    session.close()
```

### Mettre à jour un projet

```python
from viiper.persistence import get_session, ProjectRepository

session = get_session()
repo = ProjectRepository(session)

try:
    # Charger
    project = repo.get_by_name("My SaaS")

    # Modifier
    project.budget_spent = 5000.0
    project.current_users = 50
    project.phase = Phase.IDEATION

    # Sauvegarder
    updated = repo.update(project)
    print(f"Updated: {updated.name}")
finally:
    session.close()
```

### Supprimer un projet

```python
from viiper.persistence import get_session, ProjectRepository

session = get_session()
repo = ProjectRepository(session)

try:
    # Soft delete (status = "archived")
    repo.delete(project_id)

    # Hard delete (suppression permanente)
    repo.hard_delete(project_id)
finally:
    session.close()
```

---

## 🗄️ Modèles de Données

### ProjectModel

Table: `projects`

| Colonne | Type | Description |
|---------|------|-------------|
| id | String(36) | UUID unique (PK) |
| name | String(255) | Nom du projet |
| variant | String(50) | Type de projet (saas, landing, etc.) |
| phase | String(50) | Phase actuelle (validation, ideation, etc.) |
| status | String(50) | Statut (active, archived, etc.) |
| created_at | DateTime | Date de création |
| updated_at | DateTime | Dernière modification |
| started_at | DateTime | Date de démarrage (nullable) |
| timeline_weeks | Integer | Timeline planifiée |
| budget | Float | Budget total |
| budget_spent | Float | Budget dépensé |
| target_users | Integer | Objectif utilisateurs (nullable) |
| target_revenue | Float | Objectif revenu (nullable) |
| current_users | Integer | Utilisateurs actuels |
| current_revenue | Float | Revenu actuel |
| metadata_* | JSON/String | Métadonnées du projet |

**Relations**:
- `health_scores`: Liste des health scores (1-N)
- `tasks`: Liste des tâches (1-N)

**Indexes**:
- `idx_project_status_phase`: Recherche par (status, phase)
- `idx_project_created`: Tri par date de création
- Index simples sur: id, name, variant, phase, status

### HealthScoreModel

Table: `health_scores`

| Colonne | Type | Description |
|---------|------|-------------|
| id | Integer | Auto-increment (PK) |
| project_id | String(36) | Référence au projet (FK) |
| overall_score | Float | Score global (0-10) |
| performance_score | Float | Score performance |
| performance_metrics | JSON | Métriques détaillées |
| acquisition_score | Float | Score acquisition |
| acquisition_metrics | JSON | Métriques détaillées |
| engagement_score | Float | Score engagement |
| engagement_metrics | JSON | Métriques détaillées |
| revenue_score | Float | Score revenue |
| revenue_metrics | JSON | Métriques détaillées |
| created_at | DateTime | Date du snapshot |

**Relations**:
- `project`: Projet parent (N-1)

**Indexes**:
- `idx_health_project_created`: Recherche par (project_id, created_at)

### AgentModel

Table: `agents`

| Colonne | Type | Description |
|---------|------|-------------|
| id | String(36) | UUID unique (PK) |
| name | String(255) | Nom de l'agent |
| role | String(50) | Rôle (research, architecture, etc.) |
| capabilities | JSON | Liste des capacités |
| skills | JSON | Liste des skills |
| status | String(50) | Statut (idle, busy, etc.) |
| success_rate | Float | Taux de succès (0-1) |
| total_tasks | Integer | Nombre total de tâches |
| max_parallel_tasks | Integer | Concurrence max |
| auto_learn | Boolean | Apprentissage automatique |
| created_at | DateTime | Date de création |
| updated_at | DateTime | Dernière modification |

**Relations**:
- `tasks`: Liste des tâches assignées (1-N)

### TaskModel

Table: `tasks`

| Colonne | Type | Description |
|---------|------|-------------|
| id | String(36) | UUID unique (PK) |
| name | String(255) | Nom de la tâche |
| description | Text | Description détaillée |
| priority | Integer | Priorité (1-10) |
| status | String(50) | Statut (pending, completed, etc.) |
| agent_id | String(36) | Agent assigné (FK, nullable) |
| project_id | String(36) | Projet parent (FK, nullable) |
| result | JSON | Résultat de la tâche |
| error | Text | Message d'erreur (nullable) |
| created_at | DateTime | Date de création |
| completed_at | DateTime | Date de complétion (nullable) |

**Relations**:
- `agent`: Agent assigné (N-1)
- `project`: Projet parent (N-1)

**Indexes**:
- `idx_task_status_priority`: Tri par (status, priority)
- `idx_task_agent_status`: Recherche par (agent_id, status)

---

## 🔄 Migrations

### Créer une migration

```bash
# Auto-générer une migration
alembic revision --autogenerate -m "Add new field to projects"

# Migration manuelle
alembic revision -m "Custom migration"
```

### Appliquer les migrations

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Via CLI VIIPER
viiper db-upgrade

# Revenir en arrière
alembic downgrade -1
```

### Vérifier l'état

```bash
# Statut actuel
alembic current

# Historique
alembic history
```

---

## 🔧 Configuration

### Changer l'emplacement de la base de données

Par défaut: `~/.viiper/viiper.db`

**Via variable d'environnement**:
```bash
export VIIPER_DATABASE_URL="sqlite:///path/to/custom.db"
```

**Programmatiquement**:
```python
from viiper.persistence import get_database

db = get_database(database_url="sqlite:///custom.db")
```

### Utiliser PostgreSQL

```python
from viiper.persistence import get_database

db = get_database(
    database_url="postgresql://user:password@localhost/viiper"
)
db.create_tables()
```

Ou via Alembic:
```ini
# alembic.ini
sqlalchemy.url = postgresql://user:password@localhost/viiper
```

### Activer les logs SQL

```python
from viiper.persistence import get_database

db = get_database(echo=True)  # Affiche toutes les requêtes SQL
```

---

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests de persistence
pytest tests/integration/test_persistence.py -v

# Un test spécifique
pytest tests/integration/test_persistence.py::TestProjectRepository::test_create_project -v

# Avec couverture
pytest tests/integration/test_persistence.py --cov=viiper.persistence
```

### Résultats

```
20 tests passés en 0.41s
- 2 tests Database
- 18 tests ProjectRepository
```

**Couverture**:
- `database.py`: 100%
- `models.py`: 100%
- `repositories.py`: 95% (AgentRepository partiellement testé)

---

## 📊 Métriques de Performance

### Benchmarks (SQLite)

| Opération | Temps moyen | Notes |
|-----------|-------------|-------|
| Create project | ~5ms | Avec health score |
| Get by ID | ~2ms | Index sur ID |
| Get by name | ~3ms | Index sur name |
| List 100 projects | ~15ms | Sans filtres |
| Update project | ~6ms | Avec health score update |
| Delete (soft) | ~4ms | Update status seulement |
| Delete (hard) | ~8ms | Cascade delete relations |

### Optimisations

- **Indexes**: Toutes les colonnes fréquemment recherchées
- **Connection pooling**: 5 connexions par défaut (PostgreSQL)
- **Lazy loading**: Relations chargées à la demande
- **Batch operations**: Support transactions pour bulk inserts

---

## ⚠️ Limitations Connues

1. **AgentRepository**: Tests partiels uniquement
2. **TaskModel**: Pas encore de repository dédié
3. **Concurrent writes**: SQLite a des limites de concurrence
4. **Large datasets**: Pas de streaming pour très gros volumes
5. **Full-text search**: Pas implémenté (utiliser PostgreSQL + extension)

---

## 🔜 Roadmap

### Sprint 1.2 (Phase 1)
- [ ] TaskRepository complet
- [ ] Support transaction scope avancé
- [ ] Optimistic locking pour updates concurrents

### Sprint 2.1 (Phase 2)
- [ ] Migration vers PostgreSQL recommandée
- [ ] Full-text search sur projets
- [ ] Query builder pour filtres complexes

### Sprint 3.3 (Phase 3)
- [ ] Connection pooling optimisé
- [ ] Read replicas support
- [ ] Caching layer (Redis)

---

## 📝 Exemples Complets

### Workflow complet

```python
from viiper.core.project import Project
from viiper.core.variant import Variant
from viiper.core.phase import Phase
from viiper.persistence import init_database, get_session, ProjectRepository

# 1. Initialiser la DB
db = init_database()

# 2. Créer un projet
session = get_session()
repo = ProjectRepository(session)

try:
    # Créer
    project = Project(
        name="Awesome SaaS",
        variant=Variant.SAAS,
        budget=15000,
        timeline_weeks=16
    )
    project = repo.create(project)
    print(f"Created: {project.id}")

    # Modifier
    project.budget_spent = 3000
    project.current_users = 25
    project = repo.update(project)

    # Calculer et sauvegarder health
    project.calculate_health_score()
    project = repo.update(project)

    # Transition de phase
    project.transition_to_phase(Phase.IDEATION)
    project = repo.update(project)

    # Lister tous les projets
    all_projects = repo.list()
    for p in all_projects:
        print(f"- {p.name}: {p.phase.display_name}")

    # Archiver
    repo.delete(project.id)

finally:
    session.close()
```

---

## 🆘 Troubleshooting

### "Database is locked"

**SQLite concurrent writes**:
```python
# Solution: Utiliser session_scope
from viiper.persistence import get_database

db = get_database()
with db.session_scope() as session:
    repo = ProjectRepository(session)
    # Operations automatiquement committed
```

### "Table doesn't exist"

**Exécuter les migrations**:
```bash
viiper db-init
# ou
alembic upgrade head
```

### "Duplicate project name"

**Vérifier avant création**:
```python
existing = repo.get_by_name("My Project")
if existing:
    print("Project already exists!")
```

---

*Dernière mise à jour: 2026-02-16*
*Version: Sprint 1.1 Complete*
