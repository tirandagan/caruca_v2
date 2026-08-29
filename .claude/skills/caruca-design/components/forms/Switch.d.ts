/** On/off toggle for settings and run options. */
export interface SwitchProps {
  label?: React.ReactNode;
  checked?: boolean;
  disabled?: boolean;
  onChange?: (e: any) => void;
}
export declare function Switch(props: SwitchProps): JSX.Element;