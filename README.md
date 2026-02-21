# VIIPER v4

**Système Multi-Agents Autonome pour le Développement SaaS**

VIIPER (Validation → Ideation → Production → Execution → Rentabilisation → Iteration) est un framework multi-agents qui automatise le cycle complet de développement de produits SaaS, de l'idée à la monétisation.

## 🚀 Fonctionnalités

- **22 Agents Spécialisés** couvrant tout le cycle de développement
- **6 Phases Complètes** : V → I → P → E → R → I²
- **Intégration LLM Multiple** : NVIDIA GLM5, Llama 3.1, Kimi K2.5
- **Sécurité Intégrée** : Protection contre les injections de prompts et XSS
- **Pipeline Browse → Idea → Code** : De la recherche web au code déployé

## 📋 Architecture des Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIIPER FRAMEWORK v4                          │
├─────────────────────────────────────────────────────────────────┤
│  V: Validation      │ Market Research, User Interview, Browser  │
│  I: Ideation        │ System Design, Tech Stack, Security       │
│  P: Production      │ Frontend, Backend, Testing, DevOps        │
│  E: Execution       │ Marketing, Growth, Launch                 │
│  R: Rentabilisation │ Monetization, Analytics, Optimization     │
│  I²: Iteration      │ Amélioration Continue                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Agents Disponibles

### Phase V - Validation
| Agent | Description |
|-------|-------------|
| `MarketResearchAgent` | Analyse de marché et tendances |
| `UserInterviewAgent` | Interviews utilisateurs automatisées |
| `IdeaGenerationAgent` | Génération d'idées produits |
| `BrowserAgent` | Navigation web autonome et sécurisée |

### Phase I - Ideation
| Agent | Description |
|-------|-------------|
| `SystemDesignAgent` | Architecture système |
| `TechStackAgent` | Sélection de technologies |
| `SecurityPlanningAgent` | Planification sécurité |

### Phase P - Production
| Agent | Description |
|-------|-------------|
| `FrontendAgent` | Développement frontend |
| `BackendAgent` | Développement backend |
| `TestingAgent` | Tests automatisés |
| `DevOpsAgent` | Déploiement et infrastructure |

### Phase E - Execution
| Agent | Description |
|-------|-------------|
| `MarketingAgent` | Stratégie marketing |
| `GrowthAgent` | Croissance et acquisition |
| `LaunchAgent` | Lancement produit |

### Phase R - Rentabilisation
| Agent | Description |
|-------|-------------|
| `MonetizationAgent` | Modèles de monétisation |
| `AnalyticsAgent` | Analyse de données |
| `OptimizationAgent` | Optimisation performances |

### Elite & Specialist
| Agent | Description |
|-------|-------------|
| `EliteFrontendAgent` | Design world-class |
| `EliteSystemDesignAgent` | Architecture enterprise |
| `SEOAgent` | Optimisation SEO |
| `ContentWriterAgent` | Génération de contenu |

## 🔒 Sécurité

VIIPER intègre un module de sécurité complet :

```python
from viiper.security import (
    PromptInjectionGuard,  # Protection injection prompts
    ContentFilter,         # Filtrage XSS/scripts
    sanitize_url,          # Validation URLs
    validate_search_query  # Validation requêtes
)
```

**40+ patterns d'attaque détectés** :
- Injection de prompts
- Manipulation de rôle
- Override d'instructions
- XSS et scripts malveillants
- SQL injection

## 🤖 Intégration LLM

| Provider | Model | Utilisation |
|----------|-------|-------------|
| NVIDIA | `z-ai/glm5` | Code, architecture, analyse |
| NVIDIA | `llama-3.1-405b` | Raisonnement complexe |
| Kimi | `kimi-k2.5` | Recherche, idées, browsing |

```python
from viiper.llm import UnifiedLLM

# Sélection automatique du meilleur modèle
llm = UnifiedLLM()
response = llm.complete("Génère une architecture pour...")

# Modèle spécifique
llm = UnifiedLLM(model="z-ai/glm5")
```

## 📦 Installation

```bash
# Cloner le repository
git clone https://github.com/votre-repo/viiper-v4.git
cd viiper-v4

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Installer Playwright (pour BrowserAgent)
pip install playwright
playwright install
```

## 🚀 Utilisation Rapide

```python
from viiper.agents import AgentFactory

# Créer une équipe pour une phase
validation_team = AgentFactory.create_agents_for_phase("validation")
production_team = AgentFactory.create_agents_for_phase("production")

# Créer un agent spécifique
browser = AgentFactory.create_agent("browser")
idea_gen = AgentFactory.create_agent("idea_generation")

# Pipeline complet
pipeline = AgentFactory.create_browse_idea_code_pipeline()
```

## 📁 Structure du Projet

```
viiper-v4/
├── viiper/
│   ├── agents/          # 22 agents spécialisés
│   ├── core/            # Phases, projets, quality gates
│   ├── orchestrator/    # Orchestration multi-agents
│   ├── llm/             # Intégration LLM unifiée
│   ├── security/        # Protection anti-injection
│   ├── skills/          # 50+ skills réutilisables
│   ├── persistence/     # Base de données
│   ├── ckb/             # Base de connaissances collective
│   └── cli/             # Interface ligne de commande
├── tests/               # Tests unitaires et intégration
├── examples/            # Exemples d'utilisation
└── docs/                # Documentation
```

## 🧪 Tests

```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Coverage
pytest --cov=viiper tests/
```

## 📈 Métriques

| Metric | Value |
|--------|-------|
| Agents | 22 |
| Phases | 6 |
| Skills | 50+ |
| Lignes de code | ~40,000 |
| Patterns sécurité | 40+ |

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - Voir [LICENSE](LICENSE)

---

**VIIPER v4** - *Du concept à la rentabilisation, automatisé.*