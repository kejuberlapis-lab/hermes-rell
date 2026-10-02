//+------------------------------------------------------------------+
//|               Forex_Sarjana_DayScalper_07to18.mq5                |
//|               Hermes AI Agent - Professional Trader Engine       |
//|      Specialized Day-Scalper (07.00 - 18.00 WIB | Lot 0.01 Fixed)|
//+------------------------------------------------------------------+
#property copyright "Forex Sarjana & Hermes Agent"
#property link      "https://github.com/ahmdd4vd/apos"
#property version   "2.00"
#property description "EA Day-Scalper M5 Khusus Jam 07.00 - 18.00 WIB (Lot 0.01 Fixed & Model 4 MM)"

#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\OrderInfo.mqh>

CTrade         m_tradeA;
CTrade         m_tradeB;
CPositionInfo  m_position;

//--- INPUT PARAMETERS ---
input group "=== JAM OPERASIONAL (WIB / UTC+7) ==="
input int      InpBrokerGMTOffset        = 2;           // GMT Offset Server Broker (Standar: 2 atau 3)
input int      InpStartHourWIB           = 7;           // Jam Mulai Aktif (07.00 WIB)
input int      InpEndHourWIB             = 18;          // Jam Berhenti Buka Posisi Baru (18.00 WIB)
input bool     InpCloseAllAtEndHour      = false;       // Tutup Paksa Posisi Jam 18.00 WIB

input group "=== RISK & LOT SETTINGS ==="
input double   InpFixedLot               = 0.01;        // Lot Tetap per Posisi (Dibuka 2 Posisi Split = 0.02 Lot)
input double   InpMaxSpreadPoints        = 30.0;        // Maksimal Spread Toleransi (Points)

input group "=== STRATEGI & FILTER ==="
input int      InpH1_EMA_Fast            = 50;          // Fast EMA (H1)
input int      InpH1_EMA_Slow            = 200;         // Slow EMA (H1)
input int      InpM5_ATR_Period          = 14;          // ATR Periode (M5)
input double   InpM5_ATR_Multiplier_SL   = 1.0;         // Buffer Jarak SL Dinamis
input double   InpMaxCandleATRRatio      = 2.0;         // Filter Lilin Abnormal (>2.0x ATR = Skip)

input group "=== MODEL 4 TRADE MANAGEMENT ==="
input double   InpTP1_RR                 = 1.0;         // Target Posisi A (1R)
input double   InpTP2_RR                 = 3.0;         // Target Posisi B (3R Runner)
input bool     InpAutoBEP_On_TP1         = true;        // Geser SL Posisi B ke BEP saat Pos A TP

input group "=== CONFIGURASI EA ==="
input ulong    InpMagicPosA              = 999101;      // Magic Number Posisi A
input ulong    InpMagicPosB              = 999102;      // Magic Number Posisi B
input string   InpComment                = "FS_Day_07to18";

//--- GLOBAL HANDLES ---
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

   Print("EA Day-Scalper M5 (07.00 - 18.00 WIB) Siap Beroperasi!");
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
//| Konversi Waktu Server ke WIB (UTC+7)                             |
//+------------------------------------------------------------------+
int GetCurrentWIBHour()
{
   datetime serverTime = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(serverTime, dt);
   int wibHour = (dt.hour - InpBrokerGMTOffset + 7) % 24;
   if(wibHour < 0) wibHour += 24;
   return wibHour;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   int currentWIB = GetCurrentWIBHour();

   // 1. Model 4 Auto-BEP Management
   if(InpAutoBEP_On_TP1)
   {
      ManageModel4TrailingBEP();
   }

   // 2. Tutup Posisi Jam 18.00 jika diaktifkan
   if(InpCloseAllAtEndHour && currentWIB >= InpEndHourWIB)
   {
      CloseAllPositions();
      return;
   }

   // 3. Filter Jam Operasional (07.00 - 18.00 WIB)
   if(currentWIB < InpStartHourWIB || currentWIB >= InpEndHourWIB)
   {
      return;
   }

   // 4. Eksekusi Bar M5 Baru
   datetime current_bar_time = iTime(_Symbol, PERIOD_M5, 0);
   if(current_bar_time == last_bar_time) return;

   // 5. Filter Spread
   long spread = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   if(spread > InpMaxSpreadPoints) return;

   // 6. Indikator H1 & M5
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

   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   if(CopyRates(_Symbol, PERIOD_M5, 0, 5, rates) < 5) return;

   double c1_open = rates[1].open, c1_close = rates[1].close, c1_high = rates[1].high, c1_low = rates[1].low;
   double c2_open = rates[2].open, c2_close = rates[2].close, c2_high = rates[2].high, c2_low = rates[2].low;
   double c3_open = rates[3].open, c3_close = rates[3].close, c3_high = rates[3].high, c3_low = rates[3].high;

   // 7. Filter Lilin Abnormal
   if((c1_high - c1_low) > (InpMaxCandleATRRatio * m5_atr) || (c2_high - c2_low) > (InpMaxCandleATRRatio * m5_atr))
   {
      last_bar_time = current_bar_time;
      return;
   }

   if(CountMyPositions() > 0) return;

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   // 8. SETUP BUY
   bool isBullishEngulfing = (c3_close < c3_open) && (c2_close > c2_open) && (c2_open <= c3_close) && (c2_close >= c3_open);
   bool isGreenConfirmation = (c1_close > c1_open) && (c1_close > c2_close);

   if(isH1Uptrend && isBullishEngulfing && isGreenConfirmation)
   {
      double swingLow = MathMin(c1_low, MathMin(c2_low, c3_low));
      double slPrice  = NormalizeDouble(swingLow - (InpM5_ATR_Multiplier_SL * m5_atr), _Digits);
      double riskDist = ask - slPrice;

      if(riskDist > 0.40)
      {
         double tp1Price = NormalizeDouble(ask + (InpTP1_RR * riskDist), _Digits);
         double tp2Price = NormalizeDouble(ask + (InpTP2_RR * riskDist), _Digits);

         m_tradeA.Buy(InpFixedLot, _Symbol, ask, slPrice, tp1Price, InpComment + "_A");
         m_tradeB.Buy(InpFixedLot, _Symbol, ask, slPrice, tp2Price, InpComment + "_B");
         last_bar_time = current_bar_time;
         Print("[07-18 WIB] BUY Setup Model 4 Dieksekusi!");
      }
   }

   // 9. SETUP SELL
   bool isBearishEngulfing = (c3_close > c3_open) && (c2_close < c2_open) && (c2_open >= c3_close) && (c2_close <= c3_open);
   bool isRedConfirmation = (c1_close < c1_open) && (c1_close < c2_close);

   if(isH1Downtrend && isBearishEngulfing && isRedConfirmation)
   {
      double swingHigh = MathMax(c1_high, MathMax(c2_high, c3_high));
      double slPrice   = NormalizeDouble(swingHigh + (InpM5_ATR_Multiplier_SL * m5_atr) + (ask - bid), _Digits);
      double riskDist  = slPrice - bid;

      if(riskDist > 0.40)
      {
         double tp1Price = NormalizeDouble(bid - (InpTP1_RR * riskDist), _Digits);
         double tp2Price = NormalizeDouble(bid - (InpTP2_RR * riskDist), _Digits);

         m_tradeA.Sell(InpFixedLot, _Symbol, bid, slPrice, tp1Price, InpComment + "_A");
         m_tradeB.Sell(InpFixedLot, _Symbol, bid, slPrice, tp2Price, InpComment + "_B");
         last_bar_time = current_bar_time;
         Print("[07-18 WIB] SELL Setup Model 4 Dieksekusi!");
      }
   }
}

//+------------------------------------------------------------------+
//| Model 4 Auto-BEP Management                                      |
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
            if(m_position.Magic() == InpMagicPosA) hasPosA = true;
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

   if(!hasPosA && ticketPosB > 0)
   {
      if(posTypeB == POSITION_TYPE_BUY && currentSL_B < openPriceB)
      {
         m_tradeB.PositionModify(ticketPosB, openPriceB, m_position.TakeProfit());
      }
      else if(posTypeB == POSITION_TYPE_SELL && (currentSL_B > openPriceB || currentSL_B == 0))
      {
         m_tradeB.PositionModify(ticketPosB, openPriceB, m_position.TakeProfit());
      }
   }
}

//+------------------------------------------------------------------+
//| Tutup Semua Posisi                                               |
//+------------------------------------------------------------------+
void CloseAllPositions()
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(m_position.SelectByIndex(i))
      {
         if(m_position.Symbol() == _Symbol && (m_position.Magic() == InpMagicPosA || m_position.Magic() == InpMagicPosB))
         {
            CTrade trade;
            trade.PositionClose(m_position.Ticket());
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Hitung Posisi Terbuka                                            |
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
