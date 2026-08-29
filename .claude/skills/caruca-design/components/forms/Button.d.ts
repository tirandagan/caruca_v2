/** Primary action button. Sentence-case labels; hover darkens.
 * @startingPoint section="Components" subtitle="Primary, secondary, ghost, danger" viewport="700x220"
 */
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  /** Optional leading icon node (Lucide, 16px) */
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
export declare function Button(props: ButtonProps): JSX.Element;