/**
 * The console is a local instrument, never deployed (decision 1).
 *
 * `npm run dev` binds to 127.0.0.1 only. Run data embeds v1's man pages and specifications,
 * which must not reach a public location.
 */
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
export default {
  reactStrictMode: true,

  // This folder is its own project, inside a repo that has its own lockfile for the PDF
  // pipeline. Without this, Next picks the outer directory as the workspace root.
  outputFileTracingRoot: here,

  // `node:sqlite` is newer than the bundler's builtin list, so it is handed to Node directly -
  // the same issue Phase 1 hit under vitest.
  serverExternalPackages: ["node:sqlite"],

  eslint: { ignoreDuringBuilds: true },

  webpack(config) {
    // The data layer imports with explicit `.js` extensions, which is what TypeScript's
    // NodeNext resolution requires and what `tsc` and vitest both expect. Webpack does not
    // apply that mapping on its own, so it is stated here rather than by rewriting every
    // import to a form the type-checker would then reject.
    config.resolve.extensionAlias = {
      ...config.resolve.extensionAlias,
      ".js": [".ts", ".tsx", ".js"],
    };
    return config;
  },
};
