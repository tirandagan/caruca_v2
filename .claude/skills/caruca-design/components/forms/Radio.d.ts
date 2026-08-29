/** Radio button, sibling of Checkbox. */
export interface RadioProps {
  label?: React.ReactNode;
  name?: string;
  checked?: boolean;
  disabled?: boolean;
  onChange?: (e: any) => void;
}
export declare function Radio(props: RadioProps): JSX.Element;