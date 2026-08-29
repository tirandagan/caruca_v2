/** Flat white content card — hairline border, 6px radius, no shadow. */
export interface CardProps {
  title?: React.ReactNode;
  /** Right-aligned header actions */
  actions?: React.ReactNode;
  children: React.ReactNode;
  style?: React.CSSProperties;
}
export declare function Card(props: CardProps): JSX.Element;