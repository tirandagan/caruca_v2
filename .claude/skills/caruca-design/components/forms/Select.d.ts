/** Native select styled to match Input. */
export interface SelectProps {
  label?: string;
  hint?: string;
  options: Array<string | { value: string; label: string }>;
  value?: string;
  disabled?: boolean;
  onChange?: (e: any) => void;
}
export declare function Select(props: SelectProps): JSX.Element;