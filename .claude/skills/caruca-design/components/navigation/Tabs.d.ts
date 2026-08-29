/** Underline tabs — blue 2px active rule on a hairline baseline. */
export interface TabsProps {
  tabs: Array<string | { id: string; label: string; count?: number }>;
  active: string;
  onChange: (id: string) => void;
}
export declare function Tabs(props: TabsProps): JSX.Element;