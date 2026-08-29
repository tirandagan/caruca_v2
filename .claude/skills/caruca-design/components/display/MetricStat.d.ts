/** Telemetry figure: uppercase label, mono value, optional percent-change delta. */
export interface MetricStatProps {
  label: string;
  value: string | number;
  unit?: string;
  /** Percent-change roll-up, e.g. "+4.2% vs v1" */
  delta?: string;
  deltaTone?: 'up' | 'down' | 'flat';
  style?: React.CSSProperties;
}
export declare function MetricStat(props: MetricStatProps): JSX.Element;