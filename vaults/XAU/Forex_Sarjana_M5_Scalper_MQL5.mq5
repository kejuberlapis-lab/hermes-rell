//+------------------------------------------------------------------+
//|                     Forex_Sarjana_M5_Scalper.mq5                 |
//|               Hermes AI Agent - Professional Trader Engine       |
//|      Multi-Timeframe M5 Scalper (Forex Sarjana + Model 4 MM)     |
//+------------------------------------------------------------------+
#property copyright "Forex Sarjana & Hermes Agent"
#property link      "https://github.com/ahmdd4vd/apos"
#property version   "1.00"
#property description "EA Scalper Multi-Timeframe M5 (H1 Trend Filter + Model 4 Trade Management)"

#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\OrderInfo.mqh>

CTrade         m_tradeA;
CTrade         m_tradeB;
CPositionInfo  m_position;

//--- INPUT PARAMETERS ---
input group "=== MONEY MANAGEMENT ==="
input bool     InpUseAutoLot             = false;       // Gunakan Auto Risk %
input double   InpRiskPercent            = 1.0;         // Total Risiko per Setup (%)
input double   InpFixedLotPerPos         = 0.01;        // Lot Tetap per Posisi (Dibuka 2 Posisi Split)
input double   InpMaxSpreadPoints        = 35.0;        // Maksimal Spread Toleransi (Points)

input group "=== INDIKATOR & FILTER ==="
input int      InpH1_EMA_Fast            = 50;          // Fast EMA Periode (H1)
input int      InpH1_EMA_Slow            = 200;         // Slow EMA Periode (H1)
input int      InpM5_ATR_Period          = 14;          // Periode ATR (M5)
input double   InpM5_ATR_Multiplier_SL   = 1.0;         // Pengali ATR untuk Buffer Stop Loss
input double   InpMaxCandleATRRatio      = 2.0;         // Filter Lilin Abnormal (>2.0x ATR = Skip)

input group "=== MODEL 4 TRADE MANAGEMENT ==="
input double   InpTP1_RR                 = 1.0;         // Target Posisi A (1R)
input double   InpTP2_RR                 = 3.0;         // Target Posisi B (3R Runner)
input bool     InpAutoBEP_On_TP1         = true;        // Geser SL Posisi B ke BEP saat Posisi A TP

input group "=== CONFIGURASI EA ==="
input ulong    InpMagicPosA              = 888101;      // Magic Number Posisi A
input ulong    InpMagicPosB              = 888102;      // Magic Number Posisi B
input string   InpComment                = "FS_M5_MQL5";

//--- HANDLES INDIKATOR ---
int handle_h1_ema50;
int handle_h1_ema200;
int handle_m5_atr;
datetime last_bar_time = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   m_tradeA.SetExpertMagicNumber(InpMagicPosA);
   m_tradeB.SetExpertMagicNumber(InpMagicPosB);
   
   handle_h1_ema50  = iMA(_Symbol, PERIOD_H1, InpH1_EMA_Fast, 0, MODE_EMA, PRICE_CLOSE);
   handle_h1_ema200 = iMA(_Symbol, PERIOD_H1, InpH1_EMA_Slow, 0, MODE_EMA, PRICE_CLOSE);
   handle_m5_atr    = iATR(_Symbol, PERIOD_M5, InpM5_ATR_Period);

   if(handle_h1_ema50 == INVALID_HANDLE || handle_h1_ema200 == INVALID_HANDLE || handle_m5_atr == INVALID_HANDLE)
   {
      Print("Gagal menginisialisasi handle indikator!");
      return(INIT_FAILED);
   }

   Print("Forex Sarjana M5 Scalper EA (MQL5) Siap Beroperasi!");
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   IndicatorRelease(handle_h1_ema50);
   IndicatorRelease(handle_h1_ema200);
   IndicatorRelease(handle_m5_atr);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   // 1. Kelola Posisi Aktif (Model 4: Geser Posisi B ke BEP saat Posisi A Close TP)
   if(InpAutoBEP_On_TP1)
   {
      ManageModel4TrailingBEP();
   }

   // 2. Hanya eksekusi pada pembukaan Bar M5 baru
   datetime current_bar_time = iTime(_Symbol, PERIOD_M5, 0);
   if(current_bar_time == last_bar_time) return;

   // 3. Filter Spread
   long spread = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   if(spread > InpMaxSpreadPoints) return;

   // 4. Baca Nilai Indikator
   double ema50_val[], ema200_val[], atr_val[];
   ArraySetAsSeries(ema50_val, true);
   ArraySetAsSeries(ema200_val, true);
   ArraySetAsSeries(atr_val, true);

   if(CopyBuffer(handle_h1_ema50, 0, 1, 1, ema50_val) <= 0) return;
   if(CopyBuffer(handle_h1_ema200, 0, 1, 1, ema200_val) <= 0) return;
   if(CopyBuffer(handle_m5_atr, 0, 1, 1, atr_val) <= 0) return;

   bool isH1Uptrend   = (ema50_val[0] > ema200_val[0]);
   bool isH1Downtrend = (ema50_val[0] < ema200_val[0]);
   double m5_atr      = atr_val[0];

   // 5. Baca Candlestick M5 (Bar 1, Bar 2, Bar 3)
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   if(CopyRates(_Symbol, PERIOD_M5, 0, 5, rates) < 5) return;

   double c1_open = rates[1].open, c1_close = rates[1].close, c1_high = rates[1].high, c1_low = rates[1].low;
   double c2_open = rates[2].open, c2_close = rates[2].close, c2_high = rates[2].high, c2_low = rates[2].low;
   double c3_open = rates[3].open, c3_close = rates[3].close, c3_low = rates[3].low, c3_high = rates[3].high;

   // 6. Filter Lilin Abnormal
   double c1_range = c1_high - c1_low;
   double c2_range = c2_high - c2_low;
   if(c1_range > (InpMaxCandleATRRatio * m5_atr) || c2_range > (InpMaxCandleATRRatio * m5_atr))
   {
      last_bar_time = current_bar_time;
      return;
   }

   // 7. Cek Jumlah Posisi Aktif
   if(CountMyPositions() > 0) return;

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   // 8. SETUP BUY (H1 Uptrend + Bullish Engulfing + Candle Konfirmasi Hijau)
   bool isBullishEngulfing = (c3_close < c3_open) && (c2_close > c2_open) && (c2_open <= c3_close) && (c2_close >= c3_open);
   bool isGreenConfirmation = (c1_close > c1_open) && (c1_close > c2_close);

   if(isH1Uptrend && isBullishEngulfing && isGreenConfirmation)
   {
      double swingLow = MathMin(c1_low, MathMin(c2_low, c3_low));
      double slPrice  = NormalizeDouble(swingLow - (InpM5_ATR_Multiplier_SL * m5_atr), _Digits);
      double riskDist = ask - slPrice;

      if(riskDist > 0)
      {
         double tp1Price = NormalizeDouble(ask + (InpTP1_RR * riskDist), _Digits);
         double tp2Price = NormalizeDouble(ask + (InpTP2_RR * riskDist), _Digits);
         double lotSize  = CalculateLot(riskDist);

         m_tradeA.Buy(lotSize, _Symbol, ask, slPrice, tp1Price, InpComment + "_A");
         m_tradeB.Buy(lotSize, _Symbol, ask, slPrice, tp2Price, InpComment + "_B");
         last_bar_time = current_bar_time;
         Print("BUY Setup Model 4 Berhasil Dieksekusi!");
      }
   }

   // 9. SETUP SELL (H1 Downtrend + Bearish Engulfing + Candle Konfirmasi Merah)
   bool isBearishEngulfing = (c3_close > c3_open) && (c2_close < c2_open) && (c2_open >= c3_close) && (c2_close <= c3_open);
   bool isRedConfirmation = (c1_close < c1_open) && (c1_close < c2_close);

   if(isH1Downtrend && isBearishEngulfing && isRedConfirmation)
   {
      double swingHigh = MathMax(c1_high, MathMax(c2_high, c3_high));
      double slPrice   = NormalizeDouble(swingHigh + (InpM5_ATR_Multiplier_SL * m5_atr) + (ask - bid), _Digits);
      double riskDist  = slPrice - bid;

      if(riskDist > 0)
      {
         double tp1Price = NormalizeDouble(bid - (InpTP1_RR * riskDist), _Digits);
         double tp2Price = NormalizeDouble(bid - (InpTP2_RR * riskDist), _Digits);
         double lotSize  = CalculateLot(riskDist);

         m_tradeA.Sell(lotSize, _Symbol, bid, slPrice, tp1Price, InpComment + "_A");
         m_tradeB.Sell(lotSize, _Symbol, bid, slPrice, tp2Price, InpComment + "_B");
         last_bar_time = current_bar_time;
         Print("SELL Setup Model 4 Berhasil Dieksekusi!");
      }
   }
}

//+------------------------------------------------------------------+
//| Model 4 Trade Management: Geser SL Posisi B ke BEP               |
//+------------------------------------------------------------------+
void ManageModel4TrailingBEP()
{
   bool hasPosA = false;
   ulong ticketPosB = 0;
   double openPriceB = 0;
   double currentSL_B = 0;
   ENUM_POSITION_TYPE posTypeB = POSITION_TYPE_BUY;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(m_position.SelectByIndex(i))
      {
         if(m_position.Symbol() == _Symbol)
         {
            if(m_position.Magic() == InpMagicPosA)
            {
               hasPosA = true;
            }
            else if(m_position.Magic() == InpMagicPosB)
            {
               ticketPosB  = m_position.Ticket();
               openPriceB  = m_position.PriceOpen();
               currentSL_B = m_position.StopLoss();
               posTypeB    = m_position.PositionType();
            }
         }
      }
   }

   // Jika Posisi A sudah TP (tidak ada lagi di daftar posisi aktif)
   if(!hasPosA && ticketPosB > 0)
   {
      if(posTypeB == POSITION_TYPE_BUY && currentSL_B < openPriceB)
      {
         m_tradeB.PositionModify(ticketPosB, openPriceB, m_position.TakeProfit());
         Print("Posisi A Hit TP1 -> Stop Loss Posisi B Berhasil Digeser ke BEP (", openPriceB, ")");
      }
      else if(posTypeB == POSITION_TYPE_SELL && (currentSL_B > openPriceB || currentSL_B == 0))
      {
         m_tradeB.PositionModify(ticketPosB, openPriceB, m_position.TakeProfit());
         Print("Posisi A Hit TP1 -> Stop Loss Posisi B Berhasil Digeser ke BEP (", openPriceB, ")");
      }
   }
}

//+------------------------------------------------------------------+
//| Hitung Lot Size                                                  |
//+------------------------------------------------------------------+
double CalculateLot(double riskDistance)
{
   if(!InpUseAutoLot) return InpFixedLotPerPos;

   double riskMoney = AccountInfoDouble(ACCOUNT_BALANCE) * (InpRiskPercent / 100.0) / 2.0;
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

   if(tickSize <= 0 || tickValue <= 0 || riskDistance <= 0) return InpFixedLotPerPos;

   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

   double rawLot = (riskMoney / (riskDistance / tickSize * tickValue));
   double lot = MathFloor(rawLot / step) * step;

   if(lot < minLot) lot = minLot;
   if(lot > maxLot) lot = maxLot;

   return lot;
}

//+------------------------------------------------------------------+
//| Hitung Total Posisi Terbuka EA                                   |
//+------------------------------------------------------------------+
int CountMyPositions()
{
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(m_position.SelectByIndex(i))
      {
         if(m_position.Symbol() == _Symbol && (m_position.Magic() == InpMagicPosA || m_position.Magic() == InpMagicPosB))
         {
            count++;
         }
      }
   }
   return count;
}
