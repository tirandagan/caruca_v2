/** Text input with label and hint/error line. */
export interface InputProps {
  label?: string;
  hint?: string;
  /** Error message; also turns the border red */
  error?: string;
  /** JetBrains Mono value — use for commands, paths, flags */
  mono?: boolean;
  placeholder?: string;
  value?: string;
  disabled?: boolean;
  onChange?: (e: any) => void;
}
export declare function Input(props: InputProps): JSX.Element;