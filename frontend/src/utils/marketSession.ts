export type MarketSessionStatus = 'CLOSED' | 'PRE_OPEN' | 'OPEN';

export const getIndianMarketSession = (): MarketSessionStatus => {
  const now = new Date();
  
  // Format the current time in Asia/Kolkata
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Kolkata',
    weekday: 'short',
    hour: 'numeric',
    minute: 'numeric',
    hour12: false,
  });

  const parts = formatter.formatToParts(now);
  
  let weekday = '';
  let hour = 0;
  let minute = 0;

  for (const part of parts) {
    if (part.type === 'weekday') weekday = part.value;
    if (part.type === 'hour') hour = parseInt(part.value, 10);
    if (part.type === 'minute') minute = parseInt(part.value, 10);
  }

  // Weekends
  if (weekday === 'Sat' || weekday === 'Sun') {
    return 'CLOSED';
  }

  const timeInMinutes = hour * 60 + minute;
  const preOpenStart = 9 * 60; // 09:00
  const openStart = 9 * 60 + 15; // 09:15
  const openEnd = 15 * 60 + 30; // 15:30

  if (timeInMinutes >= preOpenStart && timeInMinutes < openStart) {
    return 'PRE_OPEN';
  }
  
  if (timeInMinutes >= openStart && timeInMinutes < openEnd) {
    return 'OPEN';
  }

  return 'CLOSED';
};
