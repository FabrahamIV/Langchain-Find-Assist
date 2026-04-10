# Design System Specification: The Cognitive Sanctuary

This design system serves as the foundational blueprint for a premier AI interface. It is designed to move beyond the cold, utilitarian "dashboard" aesthetic of first-generation AI and instead foster a "Cognitive Sanctuary"—a space where clarity of thought and the fluid exchange of ideas are paramount.

---

### 1. Overview & Creative North Star: "The Digital Curator"
The Creative North Star for this system is **The Digital Curator**. Unlike standard chatbots that feel like a command terminal, this system treats the conversation as an editorial layout. We achieve a premium feel through **Intentional Asymmetry** and **Tonal Depth**.

By utilizing "White Space as a Feature" rather than a void, we direct the user’s focus toward the AI’s responses. We avoid the "boxed-in" feeling of traditional templates by using overlapping layers and varying container widths to create a rhythm that mimics natural human thought.

---

### 2. Colors: Tonal Sophistication
This palette relies on high-end slates and deep blues to convey authority and trust.

*   **Primary (`#005db5`):** Used sparingly for key interactions and active states. It represents the "spark" of intelligence.
*   **Secondary & Slate (`#526074`):** These tones provide the "Editorial" backbone, grounding the interface in professional reliability.

#### The "No-Line" Rule
**Borders are strictly prohibited for sectioning.** To define boundaries, designers must use background shifts. For example, a chat input area (`surface-container-highest`) sits on a main chat thread background (`surface`), creating a distinction through tone rather than a 1px line.

#### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, semi-opaque sheets.
*   **Main Background:** `surface` (#f7f9fb)
*   **Chat Bubbles (AI):** `surface-container-low` (#f0f4f7)
*   **Chat Bubbles (User):** `primary-container` (#d6e3ff)
*   **Sidebars/Navigation:** `surface-container` (#e8eff3)

#### The "Glass & Gradient" Rule
To add "soul," floating action buttons or the chat input header should utilize **Glassmorphism**. Apply `surface_container_lowest` at 80% opacity with a `20px` backdrop-blur. Use a subtle linear gradient (from `primary` to `primary_dim`) for the "Send" button to give it a jewel-like quality.

---

### 3. Typography: Editorial Authority
We utilize a dual-font strategy to balance character with readability.

*   **Display & Headline (Manrope):** A modern, geometric sans-serif that feels architectural. Use `display-md` (2.75rem) for welcome screens and `headline-sm` (1.5rem) for major category headers.
*   **Body & Title (Inter):** The industry standard for legibility. 
    *   **AI Responses:** `body-lg` (1rem) with a generous 1.6 line-height to prevent eye fatigue.
    *   **User Inputs:** `title-sm` (1rem) to differentiate the "voice" of the user from the "voice" of the machine.

---

### 4. Elevation & Depth: Tonal Layering
We do not use shadows to create "pop"; we use them to create "atmosphere."

*   **The Layering Principle:** Place a `surface-container-lowest` card (the purest white) on a `surface-container-low` background to create a "Natural Lift."
*   **Ambient Shadows:** For floating elements like Modals or Tooltips, use an ultra-diffused shadow: `0px 12px 32px rgba(42, 52, 57, 0.06)`. Note the use of `on_surface` (#2a3439) as the shadow tint rather than pure black.
*   **The "Ghost Border" Fallback:** If a container sits on a background of the same color, use `outline-variant` (#a9b4b9) at **15% opacity**. It should be felt, not seen.

---

### 5. Components: The Intelligence Suite

#### Buttons (The Interaction Points)
*   **Primary:** Solid `primary` background with `on_primary` text. Use `rounded-md` (0.75rem).
*   **Secondary:** `surface-container-high` background. No border.
*   **Tertiary:** Text-only using `primary` color, reserved for low-emphasis actions like "Cancel."

#### Chat Bubbles (The Narrative)
*   **User:** `primary-container` with `xl` (1.5rem) rounding on three corners and `sm` (0.25rem) on the bottom-right to create a "tail" effect.
*   **AI:** `surface-container-lowest` with a "Ghost Border" and `xl` rounding. 
*   **Prohibition:** Never use divider lines between messages. Use a `24px` vertical spacing scale to separate turns.

#### Input Fields (The Command Center)
*   **Default:** `surface-container-highest` background, `rounded-xl` (1.5rem). 
*   **Active:** Transition background to `surface_container_lowest` and apply the Ambient Shadow. The focus state is signaled by the shadow, not a heavy blue outline.

#### The "Thinking" Indicator
A custom component: Three dots using `primary_fixed_dim` that pulse with a soft Gaussian blur, suggesting the AI is "weaving" a thought rather than just "loading" data.

---

### 6. Do’s and Don'ts

#### Do
*   **Do** use asymmetrical margins (e.g., more padding on the left of an AI response) to create a sophisticated, editorial feel.
*   **Do** use `surface-dim` for inactive or "read-only" states to maintain the muted, professional palette.
*   **Do** prioritize `body-lg` for AI text; the machine's voice should be the most legible element on the screen.

#### Don't
*   **Don't** use 1px solid borders. It shatters the "Digital Curator" illusion and makes the UI look like a legacy spreadsheet.
*   **Don't** use pure black (#000000). Use `on_surface` (#2a3439) for all text to keep the contrast "soft-pro."
*   **Don't** use standard `rounded-sm`. This system requires `md` (0.75rem) and `xl` (1.5rem) to maintain its friendly, sophisticated persona.