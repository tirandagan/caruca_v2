/** Callout box lifted verbatim from the PDF pipeline: 4px left bar, tinted bg, right-only radius. */
export interface CalloutProps {
  kind?: 'info' | 'warning' | 'tip' | 'danger';
  /** Uppercase small title, e.g. "Open question" */
  title?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}
export declare function Callout(props: CalloutProps): JSX.Element;