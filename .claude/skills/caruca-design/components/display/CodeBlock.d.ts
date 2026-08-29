/** Code block with the brand's right-aligned uppercase language label. */
export interface CodeBlockProps {
  /** Language tag rendered top-right, e.g. "bash", "python" */
  language?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}
export declare function CodeBlock(props: CodeBlockProps): JSX.Element;