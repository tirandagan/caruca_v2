/** Checkbox with the source's 14px / 3px-radius / blue-check anatomy. */
export interface CheckboxProps {
  label?: React.ReactNode;
  checked?: boolean;
  disabled?: boolean;
  onChange?: (e: any) => void;
}
export declare function Checkbox(props: CheckboxProps): JSX.Element;