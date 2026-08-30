import path from "path";

/**
 * Brand foundations for the PDF pipeline.
 *
 * This file is the single source of truth for every color, type step, radius,
 * and border weight the converter draws, mirroring the Caruca design system at
 * `.claude/skills/caruca-design/` (`tokens/colors.css`, `tokens/typography.css`,
 * `tokens/spacing.css`). Token names match that system deliberately, so the two
 * can be diffed against each other by eye.
 *
 * The design system states its type scale in screen px; print states it in pt.
 * The steps correspond one to one (15px body = 11pt, 27px h2 = 20pt, 37px
 * display = 28pt), so each entry below carries its px counterpart in a comment.
 *
 * Nothing in this pipeline should hardcode a hex value. Chromium renders
 * `headerTemplate`/`footerTemplate` in a separate document that inherits none of
 * the page CSS, so those two are the sole exception: they interpolate `TOKENS`
 * as literals instead of reading the custom properties.
 */

const FONTS_DIR = path.resolve(__dirname, "fonts");

export const TOKENS = {
  color: {
    // Brand
    ink: "#0B1F33", // primary text, wordmark, logo fill
    blue: "#2563EB", // primary action, links, h2, accents
    blueHover: "#1D4ED8",
    teal: "#0E7490", // secondary accent: gradients, decorative rings

    // Neutrals (text)
    gray700: "#374151",
    gray600: "#475569",
    gray500: "#616B73",
    gray400: "#9CA3AF",

    // Surfaces
    surfacePage: "#FFFFFF",
    surfaceCode: "#F6F8FA",
    surfaceInlineCode: "#EFF1F3",
    surfaceThead: "#F1F5F9",
    surfaceZebra: "#F8FAFC",
    surfaceInfo: "#EFF6FF",

    // Borders
    borderStrong: "#D0D7DE",
    borderDefault: "#E2E8F0",
    borderSubtle: "#E5E7EB",
    borderHr: "#D1D5DB",
    borderThead: "#334155",

    // Semantic
    success: "#16A34A",
    successText: "#15803D",
    successBg: "#ECFDF5",
    warning: "#E6A817",
    warningText: "#B8860B",
    warningBg: "#FFFBEB",
    danger: "#DF2E2E",
    dangerText: "#DC2626",
    dangerBg: "#FEF2F2",
  },
  radius: {
    xs: "3px", // checkbox ticks
    sm: "4px", // inline code chips
    md: "6px", // code blocks, callouts, cards
  },
  border: {
    width: "1px",
    widthStrong: "2px",
    calloutBar: "4px",
  },
} as const;

/** The teal-to-ink accent bar: 80x4, 2px radius. One of the brand's three motifs. */
export const ACCENT_GRADIENT = `linear-gradient(to right, ${TOKENS.color.teal}, ${TOKENS.color.ink})`;

/**
 * Local `@font-face` declarations for the four faces this repo ships.
 *
 * Every document surface must use these. Lexend Deca ships in exactly 400, 600,
 * and 700 here, and in no italic cut, so `font-style: italic` on a designed
 * element produces a synthesized oblique rather than a real one; use weight or
 * color for emphasis instead and leave italics to author intent in body copy.
 */
export function fontFaceCss(): string {
  const fontsDir = FONTS_DIR.replace(/\\/g, "/");

  return `
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-Regular.ttf') format('truetype');
      font-weight: 400;
      font-style: normal;
    }
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-SemiBold.ttf') format('truetype');
      font-weight: 600;
      font-style: normal;
    }
    @font-face {
      font-family: 'Lexend Deca';
      src: url('file://${fontsDir}/LexendDeca-Bold.ttf') format('truetype');
      font-weight: 700;
      font-style: normal;
    }
    @font-face {
      font-family: 'JetBrains Mono';
      src: url('file://${fontsDir}/JetBrainsMono-Regular.woff2') format('woff2');
      font-weight: 400;
      font-style: normal;
    }
  `;
}

/** The token layer as custom properties, for any document the pipeline renders. */
export function tokensCss(): string {
  const c = TOKENS.color;

  return `
    :root {
      /* Brand */
      --ink: ${c.ink};
      --blue: ${c.blue};
      --blue-hover: ${c.blueHover};
      --teal: ${c.teal};

      /* Neutrals */
      --gray-700: ${c.gray700};
      --gray-600: ${c.gray600};
      --gray-500: ${c.gray500};
      --gray-400: ${c.gray400};

      /* Surfaces */
      --surface-page: ${c.surfacePage};
      --surface-code: ${c.surfaceCode};
      --surface-inline-code: ${c.surfaceInlineCode};
      --surface-thead: ${c.surfaceThead};
      --surface-zebra: ${c.surfaceZebra};
      --surface-info: ${c.surfaceInfo};

      /* Borders */
      --border-strong: ${c.borderStrong};
      --border-default: ${c.borderDefault};
      --border-subtle: ${c.borderSubtle};
      --border-hr: ${c.borderHr};
      --border-thead: ${c.borderThead};

      /* Semantic */
      --success: ${c.success};
      --success-text: ${c.successText};
      --success-bg: ${c.successBg};
      --warning: ${c.warning};
      --warning-text: ${c.warningText};
      --warning-bg: ${c.warningBg};
      --danger: ${c.danger};
      --danger-text: ${c.dangerText};
      --danger-bg: ${c.dangerBg};

      /* Aliases */
      --text-body: var(--ink);
      --text-secondary: var(--gray-600);
      --text-muted: var(--gray-500);
      --text-faint: var(--gray-400);
      --text-link: var(--blue);
      --accent-gradient: ${ACCENT_GRADIENT};

      /* Type */
      --font-sans: 'Lexend Deca', -apple-system, 'Segoe UI', sans-serif;
      --font-mono: 'JetBrains Mono', 'Consolas', monospace;

      /* Print type scale (px equivalent from the design system in comments) */
      --text-display: 28pt;  /* 37px */
      --text-h2: 20pt;       /* 27px */
      --text-h3: 15pt;       /* 20px */
      --text-h4: 12pt;       /* 16px */
      --text-body-size: 11pt;/* 15px */
      --text-small: 10pt;    /* 13px */
      --text-code: 9.5pt;    /* 13px */
      --text-caption: 9pt;   /* 12px */
      --text-label: 8pt;     /* 11px, uppercase micro-labels */

      /* Rhythm */
      --leading-body: 1.5;
      --leading-heading: 1.2;
      --tracking-body: 0.01em;
      --tracking-heading: -0.01em;
      --tracking-label: 0.05em;
      --tracking-thead: 0.03em;

      /* Radii and borders */
      --radius-xs: ${TOKENS.radius.xs};
      --radius-sm: ${TOKENS.radius.sm};
      --radius-md: ${TOKENS.radius.md};
      --border-w: ${TOKENS.border.width};
      --border-w-strong: ${TOKENS.border.widthStrong};
      --callout-bar: ${TOKENS.border.calloutBar};
    }
  `;
}
