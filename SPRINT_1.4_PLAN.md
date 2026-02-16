# Sprint 1.4 - Skills Library Integration

## 🎯 Objectif
Créer une bibliothèque de **70+ skills** réutilisables que les agents peuvent utiliser pour générer du code de qualité professionnelle.

---

## 📋 Scope du Sprint

### 1. Skills Library Architecture (Foundation)
**Objectif**: Infrastructure pour skills réutilisables

**Composants**:
- `viiper/skills/base.py` - Classe de base Skill
- `viiper/skills/registry.py` - Registry des skills
- `viiper/skills/loader.py` - Chargement dynamique
- `viiper/skills/categories.py` - Catégorisation

**Structure Skill**:
```python
class Skill:
    name: str
    category: SkillCategory
    description: str
    code_template: str
    dependencies: List[str]
    best_practices: List[str]
    examples: List[Dict]
```

### 2. Frontend Skills (20+ skills)
**Catégories**:

**UI Components** (8 skills)
- Button with variants (primary, secondary, ghost)
- Input with validation
- Card with hover effects
- Modal/Dialog
- Dropdown/Select
- Tabs
- Toast notifications
- Loading states

**Forms** (5 skills)
- Form validation (Zod, Yup)
- Multi-step forms
- File upload with preview
- Auto-save forms
- Form state management

**Animations** (4 skills)
- Scroll-triggered animations
- Page transitions
- Micro-interactions
- Loading skeletons

**Layout** (3 skills)
- Responsive grid system
- Sidebar navigation
- Header with mobile menu

### 3. Backend Skills (20+ skills)
**Catégories**:

**API Endpoints** (6 skills)
- REST CRUD endpoints
- GraphQL resolvers
- WebSocket handlers
- File upload endpoint
- Pagination helpers
- Rate limiting

**Database** (6 skills)
- Prisma schema patterns
- Database migrations
- Query optimization
- Connection pooling
- Transactions
- Soft delete pattern

**Authentication** (4 skills)
- JWT authentication
- OAuth 2.0 integration
- Session management
- Role-based access control (RBAC)

**Business Logic** (4 skills)
- Email service (SendGrid, Resend)
- Payment processing (Stripe)
- Background jobs (Bull, Agenda)
- Caching strategies (Redis)

### 4. DevOps Skills (10+ skills)
**Catégories**:

**Deployment** (4 skills)
- Docker containerization
- Docker Compose setup
- CI/CD pipeline (GitHub Actions)
- Environment configuration

**Monitoring** (3 skills)
- Logging setup (Winston, Pino)
- Error tracking (Sentry)
- Performance monitoring

**Infrastructure** (3 skills)
- Database backup strategies
- SSL/TLS setup
- Load balancing config

### 5. Testing Skills (10+ skills)
**Catégories**:

**Unit Testing** (4 skills)
- Component tests (React Testing Library)
- API endpoint tests (Supertest)
- Service layer tests
- Utility function tests

**Integration Testing** (3 skills)
- E2E tests (Playwright, Cypress)
- Database integration tests
- API integration tests

**Testing Utilities** (3 skills)
- Test fixtures/factories
- Mocking strategies
- Test data generators

### 6. Data/ML Skills (10+ skills)
**Catégories**:

**Data Processing** (4 skills)
- CSV parsing and validation
- JSON transformation
- Data cleaning pipelines
- Batch processing

**Analytics** (3 skills)
- Event tracking (Mixpanel, Amplitude)
- A/B testing setup
- Analytics dashboard queries

**ML Integration** (3 skills)
- OpenAI API integration
- Image processing (Sharp)
- Text analysis pipelines

---

## 🏗️ Implementation Plan

### Phase 1: Infrastructure (2 hours)
**Tasks**:
- [ ] Create `viiper/skills/` directory structure
- [ ] Implement base Skill class
- [ ] Create SkillRegistry
- [ ] Add skill categories enum
- [ ] Create SkillLoader for dynamic loading

**Deliverables**:
- Base infrastructure complete
- Tests for registry and loader

### Phase 2: Frontend Skills (3 hours)
**Tasks**:
- [ ] Create 20+ frontend skills
- [ ] Organize by category
- [ ] Add code templates with best practices
- [ ] Include examples for each skill

**Deliverables**:
- `viiper/skills/frontend/` with 20+ skills
- Tests for skill loading

### Phase 3: Backend Skills (3 hours)
**Tasks**:
- [ ] Create 20+ backend skills
- [ ] Add database patterns
- [ ] Authentication flows
- [ ] API endpoint templates

**Deliverables**:
- `viiper/skills/backend/` with 20+ skills
- Integration tests

### Phase 4: DevOps & Testing Skills (2 hours)
**Tasks**:
- [ ] Create 10+ DevOps skills
- [ ] Create 10+ Testing skills
- [ ] Add deployment configurations
- [ ] Add testing utilities

**Deliverables**:
- `viiper/skills/devops/` with 10+ skills
- `viiper/skills/testing/` with 10+ skills

### Phase 5: Data/ML Skills (2 hours)
**Tasks**:
- [ ] Create 10+ Data/ML skills
- [ ] Add data processing pipelines
- [ ] Analytics integrations
- [ ] ML service wrappers

**Deliverables**:
- `viiper/skills/data/` with 10+ skills

### Phase 6: Agent Integration (2 hours)
**Tasks**:
- [ ] Extend Agent base class with skill usage
- [ ] Update agents to leverage skills
- [ ] Create skill recommendation system
- [ ] Add skill composition logic

**Deliverables**:
- Agents can query and use skills
- Tests for skill integration

### Phase 7: Collective Knowledge Base (CKB) (2 hours)
**Tasks**:
- [ ] Create CKB data structure
- [ ] Implement learning mechanism
- [ ] Add skill effectiveness tracking
- [ ] Create CKB query interface

**Deliverables**:
- CKB system operational
- Agents learn from skill usage

### Phase 8: Documentation & Testing (2 hours)
**Tasks**:
- [ ] Document all skills
- [ ] Create skills catalog
- [ ] Add usage examples
- [ ] Comprehensive tests

**Deliverables**:
- `docs/skills_library.md`
- 95%+ test coverage

---

## 📊 Success Metrics

### Quantitative
- ✅ **70+ skills** créés et testés
- ✅ **95%+ test coverage** pour skills
- ✅ **100% skills** documentés
- ✅ **Agents utilisent** skills automatiquement

### Qualitative
- ✅ Skills suivent **best practices** de l'industrie
- ✅ Code généré est **production-ready**
- ✅ Skills sont **composables** (peuvent se combiner)
- ✅ CKB **apprend** et s'améliore

---

## 🎨 Exemple de Skill

### Button Component Skill

```python
from viiper.skills.base import Skill, SkillCategory

class ButtonComponentSkill(Skill):
    name = "React Button Component"
    category = SkillCategory.FRONTEND_COMPONENTS
    description = "Premium button component with variants and accessibility"

    dependencies = [
        "react",
        "tailwindcss",
        "class-variance-authority"
    ]

    code_template = '''
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-all focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-black text-white hover:bg-gray-800 active:scale-95",
        secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
        ghost: "hover:bg-gray-100 text-gray-700",
        danger: "bg-red-600 text-white hover:bg-red-700"
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-11 px-5 text-base",
        lg: "h-13 px-7 text-lg"
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
)

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  children: React.ReactNode
  loading?: boolean
}

export function Button({
  className,
  variant,
  size,
  loading,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="animate-spin mr-2">⏳</span>
      ) : null}
      {children}
    </button>
  )
}
'''

    best_practices = [
        "Use semantic HTML (button element)",
        "Include focus states for accessibility",
        "Add loading state for async actions",
        "Use class-variance-authority for type-safe variants",
        "Follow disabled attribute convention",
        "Add active state with scale transform"
    ]

    examples = [
        {
            "name": "Primary CTA",
            "code": '<Button variant="primary">Get Started</Button>'
        },
        {
            "name": "Loading state",
            "code": '<Button loading={isLoading}>Save Changes</Button>'
        },
        {
            "name": "Ghost variant",
            "code": '<Button variant="ghost" size="sm">Cancel</Button>'
        }
    ]
```

---

## 🔄 Integration avec Agents

### Agent utilise Skills

```python
from viiper.agents.production import FrontendAgent
from viiper.skills.registry import SkillRegistry

class FrontendAgent(Agent):
    async def execute_task(self, task: AgentTask):
        # Agent query skills based on task
        relevant_skills = SkillRegistry.search(
            category=SkillCategory.FRONTEND_COMPONENTS,
            keywords=["button", "form", "input"]
        )

        # Agent compose skills
        code = self._generate_code_using_skills(relevant_skills)

        # CKB learns from usage
        self._report_skill_effectiveness(skill, effectiveness_score)

        return code
```

---

## 📦 Deliverables Finaux

### Code
- `viiper/skills/` (70+ skills organisés)
- `viiper/ckb/` (Collective Knowledge Base)
- Tests complets (95%+ coverage)

### Documentation
- `docs/skills_library.md` (Catalog complet)
- `docs/ckb.md` (CKB guide)
- Exemples d'utilisation

### Quality
- 100% skills testés
- 100% skills documentés
- Production-ready code templates

---

## ⏱️ Estimation
**Total: 18 heures** (~2-3 jours de travail)

- Phase 1: 2h
- Phase 2: 3h
- Phase 3: 3h
- Phase 4: 2h
- Phase 5: 2h
- Phase 6: 2h
- Phase 7: 2h
- Phase 8: 2h

---

**Ready to start?** 🚀
