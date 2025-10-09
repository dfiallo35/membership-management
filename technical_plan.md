# Especificación Técnica - Refactorización del Módulo Membership a Arquitectura Hexagonal

## Información General del Proyecto

### Contexto del Sistema
Este proyecto es un **Sistema de Gestión de Gimnasios** desarrollado en Python con FastAPI. El sistema maneja múltiples gimnasios, cada uno con sus propios clientes, membresías, pagos, clases, y operaciones administrativas.

### Stack Tecnológico
- **Framework Web**: FastAPI 0.115.6
- **ORM**: SQLModel 0.0.22 (basado en SQLAlchemy)
- **Base de Datos**: PostgreSQL con asyncpg
- **Autenticación**: JWT con PyJWT
- **Inyección de Dependencias**: dependency-injector 0.8.1
- **Validación**: Pydantic
- **Scheduler**: APScheduler 3.11.0
- **Rate Limiting**: SlowAPI 0.1.9

### Arquitectura Actual
El sistema actualmente utiliza una arquitectura de capas tradicional con:
- **CRUDs**: Lógica de negocio y acceso a datos mezclada
- **Models**: Entidades de dominio y esquemas de validación
- **Database**: Configuración de conexión y sesiones
- **Security**: Autenticación y autorización

## Objetivo de la Tarea

Refactorizar el módulo `membership.py` para implementar **Clean Architecture**.

## Análisis del Módulo Actual

### Funcionalidades del Módulo Membership
El módulo actual (`cruds/membership.py`) incluye:

1. **Gestión de Membresías**:
   - Crear membresía (`POST /memberships/`)
   - Obtener membresía diaria (`GET /memberships/daily`)
   - Obtener membresía por ID (`GET /memberships/{id_membership}`)
   - Listar todas las membresías (`GET /memberships/`)
   - Actualizar membresía (`PUT /memberships/{id_membership}`)
   - Eliminar membresía (`DELETE /memberships/{id_membership}`)

2. **Reglas de Negocio**:
   - Solo puede existir una membresía diaria por gimnasio
   - No se puede eliminar una membresía que esté en uso por un cliente (vigente, sin vencer)
   - Validación de unicidad de nombres por gimnasio

3. **Modelos de Datos**:
   - `Membership`: Entidad principal
   - `MembershipCreate`: DTO para creación
   - `MembershipUpdate`: DTO para actualización
   - `MembershipPublic`: DTO para respuesta pública

### Dependencias Actuales
- `models.py`: Definiciones de entidades y DTOs
- `database.py`: Gestión de sesiones de base de datos
- `security.py`: Autenticación y autorización
- `cruds/log_operations.py`: Sistema de logging
- `cruds/tags.py`: Tags para documentación API

## Especificación de la Arquitectura Hexagonal

### Estructura de Directorios Sugerida

```
features/membership/
├── __init__.py
├── application/
│   ├── __init__.py
│   ├── dtos/
│   │   ├── __init__.py
│   │   └── membership_dtos.py
│   ├── errors/
│   │   ├── __init__.py
│   │   └── membership_errors.py
│   ├── service.py
│   └── use_cases/
│       ├── __init__.py
│       ├── create_membership.py
│       ├── get_membership.py
│       ├── get_memberships.py
│       ├── update_membership.py
│       └── delete_membership.py
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── membership.py
│   ├── enums/
│   │   ├── __init__.py
│   │   └── membership_enums.py
│   ├── object_values/
│   │   ├── __init__.py
│   │   └── membership_value_objects.py
│   ├── repository_interfaces/
│   │   ├── __init__.py
│   │   └── membership_repository.py
│   └── membership_aggregate.py
├── infrastructure/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── membership_model.py
│   └── repositories/
│       ├── __init__.py
│       └── membership_repository_postgres.py
├── presentation/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── membership_controller.py
│   └── routes/
│       ├── __init__.py
│       └── membership_routes.py
└── routes.py
```

### Capas de la Arquitectura

#### 1. Capa de Dominio (`domain/`)

**Entidades**:
- `Membership`: Entidad principal con lógica de negocio
- `MembershipId`: Value Object para identificadores
- `MembershipPrice`: Value Object para precios
- `MembershipDuration`: Value Object para duración

**Agregado**:
- `MembershipAggregate`: Agregado raíz que encapsula la entidad y sus reglas de negocio

**Interfaces de Repositorio**:
- `IMembershipRepository`: Contrato para persistencia
- `ILoggingService`: Contrato para logging

**Enums**:
- `MembershipStatus`: Estados de la membresía
- `MembershipType`: Tipos de membresía

#### 2. Capa de Aplicación (`application/`)

**DTOs**:
- `MembershipCreateRequest`: DTO para creación
- `MembershipUpdateRequest`: DTO para actualización
- `MembershipResponse`: DTO para respuestas
- `MembershipListResponse`: DTO para listados

**Casos de Uso**:
- `CreateMembershipUseCase`: Crear membresía
- `GetMembershipUseCase`: Obtener membresía
- `GetMembershipsUseCase`: Listar membresías
- `UpdateMembershipUseCase`: Actualizar membresía
- `DeleteMembershipUseCase`: Eliminar membresía

**Servicios de Aplicación**:
- `MembershipService`: Orquestador principal

**Errores**:
- `MembershipNotFoundError`: Error cuando no se encuentra
- `MembershipAlreadyExistsError`: Error de duplicación
- `MembershipInUseError`: Error cuando está en uso
- `DailyMembershipExistsError`: Error de membresía diaria duplicada

#### 3. Capa de Infraestructura (`infrastructure/`)

**Modelos de Base de Datos**:
- `MembershipModel`: Mapeo SQLModel para PostgreSQL

**Repositorios**:
- `MembershipRepositoryPostgres`: Implementación del repositorio

**Servicios Externos**:
- `LoggingService`: Implementación del logging

#### 4. Capa de Presentación (`presentation/`)

**Controladores**:
- `MembershipController`: Lógica de presentación

**Rutas**:
- `MembershipRoutes`: Definición de endpoints FastAPI

### Reglas de Negocio a Implementar

1. **Unicidad de Nombre**: No puede existir otra membresía con el mismo nombre en el mismo gimnasio
2. **Membresía Diaria Única**: Solo puede existir una membresía con `duration_days = 1` por gimnasio
3. **Validación de Eliminación**: No se puede eliminar una membresía que esté vigente (en uso)
4. **Auditoría**: Todas las operaciones deben ser registradas en el sistema de logging
5. **Autorización**: Solo usuarios con permisos adecuados pueden realizar operaciones

### Patrones de Diseño a Aplicar

1. **Repository Pattern**: Para abstraer el acceso a datos
2. **Use Case Pattern**: Para encapsular lógica de negocio
3. **DTO Pattern**: Para transferencia de datos entre capas
4. **Dependency Injection**: Para inyección de dependencias
5. **Factory Pattern**: Para creación de agregados
6. **Specification Pattern**: Para reglas de negocio complejas

## Especificaciones Técnicas Detalladas

### 1. Entidad de Dominio - Membership

```python
class Membership:
    def __init__(self, id: MembershipId, name: str, description: str,
                 duration_days: int, price: MembershipPrice,
                 is_active: bool, gym_id: UUID):
        # Validaciones de negocio
        # Invariantes del agregado
        pass

    def activate(self) -> None:
        """Activa la membresía"""
        pass

    def deactivate(self) -> None:
        """Desactiva la membresía"""
        pass

    def is_daily(self) -> bool:
        """Verifica si es una membresía diaria"""
        pass

    def can_be_deleted(self) -> bool:
        """Verifica si puede ser eliminada"""
        pass
```

### 2. Agregado de Dominio

```python
class MembershipAggregate:
    def __init__(self, membership: Membership):
        self._membership = membership
        self._events = []

    @property
    def membership(self) -> Membership:
        return self._membership

    def create(self) -> None:
        """Crea una nueva membresía"""
        pass

    def update(self, data: dict) -> None:
        """Actualiza la membresía"""
        pass

    def delete(self) -> None:
        """Elimina la membresía"""
        pass
```

### 3. Casos de Uso

```python
class CreateMembershipUseCase:
    def __init__(self, repository: IMembershipRepository,
                 logging_service: ILoggingService):
        self._repository = repository
        self._logging_service = logging_service

    async def execute(self, request: MembershipCreateRequest,
                     user_id: UUID, gym_id: UUID) -> MembershipResponse:
        # 1. Validar unicidad de nombre
        # 2. Validar membresía diaria única
        # 3. Crear agregado
        # 4. Persistir
        # 5. Log operación
        pass
```

### 4. Repositorio

```python
class IMembershipRepository(ABC):
    @abstractmethod
    async def save(self, aggregate: MembershipAggregate) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID, gym_id: UUID) -> Optional[MembershipAggregate]:
        pass

    @abstractmethod
    async def find_by_name(self, name: str, gym_id: UUID) -> Optional[MembershipAggregate]:
        pass

    @abstractmethod
    async def find_daily_membership(self, gym_id: UUID) -> Optional[MembershipAggregate]:
        pass

    @abstractmethod
    async def find_all(self, gym_id: UUID) -> List[MembershipAggregate]:
        pass

    @abstractmethod
    async def delete(self, id: UUID, gym_id: UUID) -> bool:
        pass

    @abstractmethod
    async def is_membership_in_use(self, id: UUID, gym_id: UUID) -> bool:
        pass
```

## Criterios de Evaluación

### 1. Arquitectura (40%)
- ✅ Separación clara de capas
- ✅ Inversión de dependencias correcta
- ✅ Interfaces bien definidas
- ✅ Agregados de dominio apropiados
- ✅ Value Objects implementados

### 2. Código (30%)
- ✅ Código limpio y legible
- ✅ Nombres descriptivos
- ✅ Funciones pequeñas y enfocadas
- ✅ Manejo de errores apropiado
- ✅ Documentación de código

### 3. Funcionalidad (20%)
- ✅ Todas las operaciones CRUD implementadas
- ✅ Reglas de negocio respetadas
- ✅ Validaciones correctas
- ✅ Logging implementado
- ✅ Manejo de errores HTTP

### 4. Testing (10%)
- ✅ Tests unitarios para lógica de negocio
- ✅ Tests de integración para casos de uso
- ✅ Mocks apropiados para dependencias
- ✅ Cobertura de casos edge

## Entregables Esperados

### 1. Código Fuente
- Estructura completa de directorios
- Implementación de todas las capas
- Tests unitarios e integración
- Documentación de código

### 2. Documentación
- README con instrucciones de instalación
- Diagrama de arquitectura
- Documentación de APIs
- Guía de testing

### 3. Configuración
- Archivo de configuración para inyección de dependencias
- Scripts de migración si es necesario
- Configuración de testing

## Consideraciones Especiales

### 1. Integración con el Sistema Existente
- Mantener compatibilidad con la API actual
- Reutilizar modelos existentes donde sea posible
- Integrar con el sistema de logging existente
- Mantener la misma estructura de respuestas HTTP

### 2. Performance
- Optimizar consultas de base de datos
- Implementar paginación para listados
- Usar índices apropiados
- Minimizar transferencia de datos

### 3. Seguridad
- Validar permisos en cada operación
- Sanitizar inputs
- Prevenir inyección SQL
- Logging de operaciones sensibles

### 4. Mantenibilidad
- Código fácil de entender y modificar
- Separación clara de responsabilidades
- Documentación actualizada
- Tests que faciliten refactoring

## Tiempo Estimado

**Duración**: 1 semana (5 días laborales)

**Distribución sugerida**:
- Día 1: Análisis y diseño de arquitectura
- Día 2: Implementación de capa de dominio
- Día 3: Implementación de capa de aplicación
- Día 4: Implementación de capa de infraestructura y presentación
- Día 5: Testing, documentación y refinamiento

## Recursos de Referencia

1. **Arquitectura Hexagonal**: [Ports and Adapters Pattern](https://alistair.cockburn.us/hexagonal-architecture/)
2. **Clean Architecture**: Robert C. Martin
3. **Domain-Driven Design**: Eric Evans
4. **Patrón Repository**: [Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)

## Contacto y Soporte

Para dudas técnicas durante el desarrollo, contactar al equipo del proyecto.

---

**Fecha de Emisión**: [Fecha actual]
**Versión**: 1.0
**Estado**: En desarrollo
