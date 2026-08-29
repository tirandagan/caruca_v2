/** Status pill — the only pill shape in the system. */
export interface BadgeProps {
  tone?: 'neutral' | 'info' | 'success' | 'warning' | 'danger';
  /** Leading status dot */
  dot?: boolean;
  /** Mono text (condition labels like v1-faithful) */
  mono?: boolean;
  children: React.ReactNode;
}
export declare function Badge(props: BadgeProps): JSX.Element;