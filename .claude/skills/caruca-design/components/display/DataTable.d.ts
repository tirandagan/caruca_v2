/** Comparison table: uppercase gray headers, 2px header rule, zebra rows. */
export interface DataTableColumn {
  key: string;
  label: string;
  /** Mono cells for commands/values */
  mono?: boolean;
  /** 'right' also sets mono numerals */
  align?: 'left' | 'right';
}
export interface DataTableProps {
  columns: DataTableColumn[];
  rows: Array<Record<string, React.ReactNode>>;
  style?: React.CSSProperties;
}
export declare function DataTable(props: DataTableProps): JSX.Element;