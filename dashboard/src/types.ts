export type Event = {
  id: number;
  event_type: string;
  created_at: string;
  payload: string;
};

export type AccountEvent = {
  equity: number;
  cash: number;
  buying_power: number;
  daily_pnl: number;
  open_positions: number;
};
