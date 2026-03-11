# Documento de Requisitos del Sistema  
## Sistema: Chambitas

### 1. Introducción

**Objetivo del documento**  
Este documento especifica los **requisitos funcionales** y **no funcionales** del sistema Chambitas, a partir del modelo de datos de la base de datos `chambitas`. Sirve como referencia para el equipo de análisis, desarrollo, pruebas y mantenimiento.

**Alcance**  
Chambitas es una plataforma que permite a los usuarios gestionar su perfil (incluidos datos de contacto y enlaces), publicaciones, aptitudes, intereses, recomendaciones y conversaciones privadas entre usuarios.

---

### 2. Definiciones y términos

- **Usuario**: Persona registrada en la plataforma.
- **Perfil**: Información ampliada del usuario (descripción/bio, número de teléfono, WhatsApp) y enlaces asociados (redes, portafolio, etc.). Relación 1:1 con Usuario.
- **Link**: Enlace (URL) asociado a un perfil (redes sociales, portafolio, etc.). Un perfil puede tener varios enlaces.
- **Publicación**: Contenido creado por el usuario (texto e imagen).
- **Reacción**: Interacción de un usuario sobre una publicación (p. ej. “me gusta”).
- **Comentario**: Mensaje asociado a una publicación.
- **Aptitud**: Habilidad o competencia de un usuario.
- **Interés**: Tema o área de interés de un usuario.
- **Recomendación**: Referencia o valoración que un usuario realiza sobre otro.
- **Conversación**: Canal de mensajería entre dos usuarios.
- **Mensaje**: Comunicación textual enviada dentro de una conversación.

---

### 3. Requisitos funcionales

#### 3.1. Gestión de usuarios

**RF-01 – Registro de usuario**  
El sistema debe permitir el registro de nuevos usuarios almacenando al menos:
- Nombre.
- Correo electrónico único.
- Contraseña (almacenada de forma cifrada/hasheada).
- Opcionalmente: fecha de nacimiento y ubicación.

**RF-02 – Autenticación de usuario**  
El sistema debe permitir que un usuario se autentique mediante:
- Correo electrónico.
- Contraseña válida asociada a dicho correo.

**RF-03 – Gestión del estado de usuario**  
El sistema debe permitir marcar a un usuario como:
- `activo`: usuario con acceso normal a la plataforma.
- `inactivo`: usuario sin acceso, manteniendo su información para historial o reactivación.

**RF-04 – Actualización de datos de usuario**  
El sistema debe permitir la actualización de los datos personales del usuario (nombre, fecha de nacimiento, ubicación, correo).

---

#### 3.2. Gestión de perfil y datos de contacto

**RF-05 – Creación y asociación de perfil**  
El sistema debe permitir crear un perfil 1:1 para cada usuario, con:
- Descripción o biografía.
- Número de teléfono (opcional).
- Número o identificador de WhatsApp (opcional).

**RF-06 – Edición de perfil**  
El sistema debe permitir al usuario editar los datos de su perfil: descripción, número de teléfono y WhatsApp.

**RF-07 – Eliminación de usuario y perfil asociado**  
Al eliminar un usuario, el sistema debe eliminar automáticamente su perfil asociado y todos los enlaces (Links) de ese perfil.

**RF-08 – Asociar enlaces al perfil**  
El sistema debe permitir registrar uno o varios enlaces (URLs) asociados al perfil del usuario (redes sociales, portafolio, etc.).

**RF-09 – Edición y eliminación de enlaces**  
El sistema debe permitir modificar y eliminar enlaces del perfil.

**RF-10 – Eliminación en cascada de enlaces**  
Al eliminar un perfil (o al eliminar el usuario), el sistema debe eliminar automáticamente todos los enlaces asociados a dicho perfil.

---

#### 3.3. Gestión de publicaciones

**RF-11 – Creación de publicaciones**  
El sistema debe permitir que los usuarios creen publicaciones con:
- Descripción textual.
- Imagen opcional.
- Registro de fecha y hora de creación.

**RF-12 – Edición de publicaciones**  
El sistema debe permitir que el autor de una publicación actualice su contenido (texto e imagen), registrando la fecha de actualización.

**RF-13 – Eliminación de publicaciones**  
El sistema debe permitir que el autor (o un administrador autorizado) elimine una publicación.

**RF-14 – Eliminación en cascada de interacciones**  
Al eliminar una publicación, el sistema debe eliminar automáticamente:
- Reacciones asociadas.
- Comentarios asociados.

---

#### 3.4. Reacciones y comentarios

**RF-15 – Registrar reacciones**  
El sistema debe permitir que un usuario registre una reacción sobre una publicación.

**RF-16 – Registro de comentarios**  
El sistema debe permitir que un usuario comente una publicación, registrando la fecha de creación del comentario.

**RF-17 – Eliminación en cascada de reacciones y comentarios**  
Al eliminar un usuario, el sistema debe eliminar automáticamente las reacciones y comentarios asociados a dicho usuario. Al eliminar una publicación, se deben eliminar las reacciones y comentarios asociados a ella.

---

#### 3.5. Gestión de aptitudes

**RF-18 – Catálogo de aptitudes**  
El sistema debe permitir mantener un catálogo de aptitudes (crear, consultar, modificar, eliminar).

**RF-19 – Asociación de aptitudes a usuarios**  
El sistema debe permitir asociar múltiples aptitudes a un mismo usuario.

**RF-20 – Desasociación de aptitudes**  
El sistema debe permitir eliminar la relación entre un usuario y una aptitud concreta sin borrar necesariamente la aptitud del catálogo.

---

#### 3.6. Gestión de intereses

**RF-21 – Catálogo de intereses**  
El sistema debe permitir mantener un catálogo de intereses (crear, consultar, modificar, eliminar).

**RF-22 – Asociación de intereses a usuarios**  
El sistema debe permitir asociar múltiples intereses a un mismo usuario.

**RF-23 – Desasociación de intereses**  
El sistema debe permitir eliminar la relación entre un usuario y un interés concreto sin borrar necesariamente el interés del catálogo.

---

#### 3.7. Recomendaciones entre usuarios

**RF-24 – Emisión de recomendaciones**  
El sistema debe permitir que un usuario emita una recomendación sobre otro usuario, almacenando:
- Usuario emisor.
- Usuario receptor.
- Contenido textual de la recomendación.
- Fechas de creación y actualización.

**RF-25 – Consulta de recomendaciones recibidas**  
El sistema debe permitir que un usuario consulte las recomendaciones que otros usuarios han emitido sobre él.

---

#### 3.8. Mensajería y conversaciones

**RF-26 – Creación de conversaciones**  
El sistema debe permitir crear una conversación entre dos usuarios, registrando:
- Usuario emisor inicial.
- Usuario receptor.
- Fecha y hora de creación.

**RF-27 – Envío de mensajes**  
El sistema debe permitir enviar mensajes dentro de una conversación, registrando:
- Usuario emisor.
- Contenido del mensaje.
- Fecha y hora de envío.

**RF-28 – Eliminación de conversaciones**  
Al eliminar una conversación, el sistema debe eliminar automáticamente todos los mensajes asociados a ella.

---

### 4. Requisitos no funcionales

> Nota: estos requisitos se infieren del modelo de datos y del contexto; deberán completarse con decisiones de arquitectura e infraestructura.

#### 4.1. Seguridad

**RNF-01 – Confidencialidad de contraseñas**  
Las contraseñas de los usuarios deben almacenarse cifradas/hasheadas utilizando algoritmos de hashing seguro (por ejemplo, bcrypt, Argon2 u otro equivalente).

**RNF-02 – Integridad de datos**  
Se deben mantener claves primarias, foráneas y restricciones únicas para asegurar la integridad referencial del modelo (Perfil → Usuario, Link → Perfil, etc.).

**RNF-03 – Control de acceso**  
El acceso a operaciones de lectura y escritura sobre la base de datos debe estar restringido mediante roles y privilegios (por ejemplo, separar usuarios de aplicación y usuarios administrativos de base de datos).

---

#### 4.2. Rendimiento y escalabilidad

**RNF-04 – Rendimiento de consultas frecuentes**  
El sistema debe poder responder en tiempos aceptables (por definir) a las operaciones más frecuentes, como:
- Consulta de publicaciones recientes.
- Consulta de reacciones y comentarios.
- Consulta de perfil (descripción, teléfono, WhatsApp, enlaces), aptitudes e intereses de un usuario.

Se recomienda definir índices apropiados sobre claves foráneas y campos de búsqueda habituales (por ejemplo, `Usuario.correo`, `Publicacion.usuario_id`, `Link.perfil_id`, etc.).

**RNF-05 – Escalabilidad moderada**  
El diseño de la base de datos debe permitir un crecimiento gradual en el número de usuarios, perfiles, publicaciones, comentarios y mensajes sin requerir cambios estructurales drásticos.

---

#### 4.3. Fiabilidad y disponibilidad

**RNF-06 – Recuperación ante fallos**  
Se deberán definir y ejecutar políticas de copias de seguridad (backups) periódicas de la base de datos, así como procedimientos de restauración para minimizar la pérdida de datos en caso de fallo.

**RNF-07 – Disponibilidad**  
La base de datos debe estar disponible conforme a los objetivos de nivel de servicio (SLA) que se definan para la plataforma (por ejemplo, % de disponibilidad mensual).

---

#### 4.4. Mantenibilidad y extensibilidad

**RNF-08 – Normalización del modelo**  
El modelo de datos debe mantenerse razonablemente normalizado (al menos hasta 3FN) para facilitar su mantenimiento y evitar redundancias innecesarias.

**RNF-09 – Extensibilidad**  
La estructura debe permitir incorporar nuevas funcionalidades (por ejemplo, nuevos tipos de reacciones, estados de conversación, adjuntos en mensajes) con impacto mínimo en el modelo existente.

---

#### 4.5. Auditoría y trazabilidad

**RNF-10 – Trazabilidad básica**  
Los campos `created_at` y `updated_at` deben mantenerse actualizados para las entidades que los incluyen, permitiendo conocer la fecha de creación y de última modificación de los registros.

---

### 5. Pendientes y definiciones futuras

- Definición detallada de políticas de seguridad (encriptación en tránsito, autenticación multifactor, etc.).
- Parámetros concretos de rendimiento (tiempos máximos de respuesta, carga concurrente esperada).
- Políticas formales de backup y recuperación.
- Reglas de negocio adicionales (por ejemplo, límites de tamaño para imágenes, longitud máxima de contenidos, moderación de comentarios).

---

*Documento alineado con el esquema de base de datos `chambitas`*
