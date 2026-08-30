import type { ThemeRegistrationRaw } from "shiki";
import { TOKENS } from "./tokens";

const c = TOKENS.color;

/**
 * Syntax highlighting in the brand's own palette.
 *
 * The pipeline previously used Shiki's `github-light`, which paints code in
 * GitHub's purples, oranges, and crimsons — six or seven hues that appear
 * nowhere in this identity, on the pages where commands and specs matter most.
 * The brand is ink plus one blue plus a teal accent, and its imagery direction
 * is "cool, technical, monochrome-plus-blue", so this theme carries four roles
 * and no more:
 *
 *   structure (keywords, control flow, tags) -> blue
 *   literals  (strings, numbers, constants)  -> teal
 *   asides    (comments)                     -> gray-500
 *   everything else (identifiers, operators) -> ink and gray-700
 *
 * Names of things being defined get weight rather than a fifth hue. Red is
 * reserved for what it means everywhere else in the system: something wrong.
 */
export const carucaSyntaxTheme: ThemeRegistrationRaw = {
  name: "caruca",
  type: "light",
  colors: {
    "editor.background": c.surfaceCode,
    "editor.foreground": c.ink,
  },
  settings: [
    {
      settings: { background: c.surfaceCode, foreground: c.ink },
    },

    // Asides
    {
      scope: ["comment", "punctuation.definition.comment", "string.comment"],
      settings: { foreground: c.gray500 },
    },

    // Structure
    {
      scope: [
        "keyword",
        "keyword.control",
        "keyword.other",
        "storage",
        "storage.type",
        "storage.modifier",
        "variable.language",
        "entity.name.tag",
        "meta.diff.header",
        "markup.heading",
      ],
      settings: { foreground: c.blue },
    },

    // Literals
    {
      scope: [
        "string",
        "string.quoted",
        "string.template",
        "punctuation.definition.string",
        "constant.character.escape",
        "constant.numeric",
        "constant.language",
        "constant.other",
        "support.constant",
        "entity.other.attribute-name",
      ],
      settings: { foreground: c.teal },
    },

    // Things being named: weight, not another hue.
    {
      scope: [
        "entity.name.function",
        "entity.name.class",
        "entity.name.type",
        "support.function",
        "support.class",
        "support.type",
      ],
      settings: { foreground: c.ink, fontStyle: "bold" },
    },

    // Identifiers and operators sit just off the body ink.
    {
      scope: [
        "variable",
        "variable.other",
        "variable.parameter",
        "keyword.operator",
        "punctuation",
        "meta.brace",
      ],
      settings: { foreground: c.gray700 },
    },

    // Semantics, used only for what they mean elsewhere in the system.
    {
      scope: ["markup.inserted", "markup.inserted.diff"],
      settings: { foreground: c.successText },
    },
    {
      scope: ["markup.deleted", "markup.deleted.diff"],
      settings: { foreground: c.dangerText },
    },
    {
      scope: ["invalid", "invalid.illegal"],
      settings: { foreground: c.danger },
    },
  ],
};

export const CARUCA_THEME_NAME = "caruca";
