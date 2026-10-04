export interface OHLCV {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export const calculateSMA = (data: OHLCV[], period: number) => {
  const result: { time: string; value: number }[] = [];
  for (let i = period - 1; i < data.length; i++) {
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += data[i - j].close;
    }
    result.push({ time: data[i].time, value: sum / period });
  }
  return result;
};

export const calculateEMA = (data: OHLCV[], period: number) => {
  const result: { time: string; value: number }[] = [];
  const multiplier = 2 / (period + 1);
  
  if (data.length < period) return result;
  
  // Start with SMA for first EMA value
  let sum = 0;
  for (let i = 0; i < period; i++) {
    sum += data[i].close;
  }
  let prevEma = sum / period;
  result.push({ time: data[period - 1].time, value: prevEma });

  for (let i = period; i < data.length; i++) {
    const ema = (data[i].close - prevEma) * multiplier + prevEma;
    result.push({ time: data[i].time, value: ema });
    prevEma = ema;
  }
  return result;
};

export const calculateRSI = (data: OHLCV[], period: number) => {
  const result: { time: string; value: number }[] = [];
  if (data.length <= period) return result;

  let gains = 0;
  let losses = 0;

  for (let i = 1; i <= period; i++) {
    const diff = data[i].close - data[i - 1].close;
    if (diff > 0) gains += diff;
    else losses -= diff;
  }

  let avgGain = gains / period;
  let avgLoss = losses / period;

  let rs = avgGain / (avgLoss === 0 ? 1e-10 : avgLoss);
  let rsi = 100 - 100 / (1 + rs);
  
  result.push({ time: data[period].time, value: avgLoss === 0 ? 100 : rsi });

  for (let i = period + 1; i < data.length; i++) {
    const diff = data[i].close - data[i - 1].close;
    const currentGain = diff > 0 ? diff : 0;
    const currentLoss = diff < 0 ? -diff : 0;

    avgGain = (avgGain * (period - 1) + currentGain) / period;
    avgLoss = (avgLoss * (period - 1) + currentLoss) / period;

    rs = avgGain / (avgLoss === 0 ? 1e-10 : avgLoss);
    rsi = 100 - 100 / (1 + rs);

    result.push({ time: data[i].time, value: avgLoss === 0 ? 100 : rsi });
  }

  return result;
};

export const calculateMACD = (data: OHLCV[], shortPeriod = 12, longPeriod = 26, signalPeriod = 9) => {
  const result: { time: string; macd: number; signal: number; histogram: number }[] = [];
  if (data.length <= longPeriod) return result;

  const shortEMA = calculateEMA(data, shortPeriod);
  const longEMA = calculateEMA(data, longPeriod);
  
  // Align the two EMAs
  const macdLine = [];
  let longIdx = 0;
  for (let i = 0; i < shortEMA.length; i++) {
    if (longIdx < longEMA.length && shortEMA[i].time === longEMA[longIdx].time) {
      macdLine.push({
        time: shortEMA[i].time,
        close: shortEMA[i].value - longEMA[longIdx].value
      });
      longIdx++;
    }
  }

  const signalEMA = calculateEMA(macdLine as any, signalPeriod);
  
  let signalIdx = 0;
  for (let i = 0; i < macdLine.length; i++) {
    if (signalIdx < signalEMA.length && macdLine[i].time === signalEMA[signalIdx].time) {
      result.push({
        time: macdLine[i].time,
        macd: macdLine[i].close,
        signal: signalEMA[signalIdx].value,
        histogram: macdLine[i].close - signalEMA[signalIdx].value
      });
      signalIdx++;
    }
  }

  return result;
};

export const calculateBollingerBands = (data: OHLCV[], period = 20, stdDev = 2) => {
  const result: { time: string; upper: number; middle: number; lower: number }[] = [];
  if (data.length < period) return result;

  for (let i = period - 1; i < data.length; i++) {
    let sum = 0;
    for (let j = 0; j < period; j++) {
      sum += data[i - j].close;
    }
    const middle = sum / period;

    let varianceSum = 0;
    for (let j = 0; j < period; j++) {
      varianceSum += Math.pow(data[i - j].close - middle, 2);
    }
    const stdDeviation = Math.sqrt(varianceSum / period);

    result.push({
      time: data[i].time,
      middle,
      upper: middle + stdDeviation * stdDev,
      lower: middle - stdDeviation * stdDev
    });
  }

  return result;
};

export const calculateATR = (data: OHLCV[], period = 14) => {
  const result: { time: string; value: number }[] = [];
  if (data.length <= period) return result;

  const trueRanges = [data[0].high - data[0].low];
  for (let i = 1; i < data.length; i++) {
    const highLow = data[i].high - data[i].low;
    const highClose = Math.abs(data[i].high - data[i - 1].close);
    const lowClose = Math.abs(data[i].low - data[i - 1].close);
    trueRanges.push(Math.max(highLow, highClose, lowClose));
  }

  let atrSum = 0;
  for (let i = 1; i <= period; i++) { // ATR starts at index period
    atrSum += trueRanges[i];
  }
  let prevATR = atrSum / period;
  result.push({ time: data[period].time, value: prevATR });

  for (let i = period + 1; i < data.length; i++) {
    const atr = (prevATR * (period - 1) + trueRanges[i]) / period;
    result.push({ time: data[i].time, value: atr });
    prevATR = atr;
  }

  return result;
};
