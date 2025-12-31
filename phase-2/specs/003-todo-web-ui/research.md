# Research: Todo Web UI Design

## Decision: Layout & Navigation Implementation

### Component Patterns
- **Layout**: Sticky header with a collapsible/sliding sidebar for mobile.
- **Task Interaction**: In-line editing or modal based on screen density. For non-technical users, clear modal dialogs for editing are preferred to avoid accidental changes.

### Palette & Typography
- **Primary**: Pink-600 (`#db2777`) for CTAs.
- **Secondary**: Pink-50 (light wash for backgrounds) and White (`#ffffff`).
- **Typography**: Inter (Sans-serif) for clean readability.

### Accessibility (WCAG AA)
- Focus indicators will use a high-contrast ring (`ring-pink-300`).
- Semantic HTML tags (main, nav, section) to be used throughout.

## Rationale
- Non-technical users benefit from "Big, Bold, Simple" UI.
- Pink provides a warm, distinguishable brand identity compared to standard blue/gray apps.

## Alternatives Considered
- **Option A (In-line editing)**: Rejected because it can be messy on mobile and confusing for non-technical users.
- **Option B (Tabbed navigation)**: Rejected in favor of a Sidebar to allow for future feature expansion without cluttering the bottom screen space.
