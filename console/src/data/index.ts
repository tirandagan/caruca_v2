/**
 * The data layer (task 010, Phase 1).
 *
 * Everything the console knows, it reads from files through this module. Nothing above it
 * parses a run directory, opens the metrics database, or reads terminal text for a number.
 */
export * from "./paths.js";
export * from "./schema.js";
export * from "./commandLine.js";
export * from "./runs.js";
export * from "./v1Runs.js";
export * from "./metricsDb.js";
export * from "./campaigns.js";
export * from "./consistency.js";
export * from "./asciicast.js";
export * from "./events.js";
export * from "./promptDrift.js";
export * from "./findings.js";
