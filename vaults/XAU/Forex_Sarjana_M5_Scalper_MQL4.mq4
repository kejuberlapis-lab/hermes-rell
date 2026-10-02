//+------------------------------------------------------------------+
//|                     Forex_Sarjana_M5_Scalper.mq4                 |
//|               Hermes AI Agent - Professional Trader Engine       |
//|      Multi-Timeframe M5 Scalper (Forex Sarjana + Model 4 MM)     |
//+------------------------------------------------------------------+
#property copyright "Forex Sarjana & Hermes Agent"
#property link      "https://github.com/ahmdd4vd/apos"
#property version   "1.00"
#property strict

//--- INPUT PARAMETERS ---
extern string   ---_RISK_SETTINGS_---       = "=== MONEY MANAGEMENT ===";
extern bool     UseAutoLot                  = false;            // Hitung Lot Otomatis berbasis % Risiko
extern double   RiskPercentPerTrade         = 1.0;              // Risiko per Trade (%) jika AutoLot aktif
extern double   FixedLotPerPosition         = 0.01;             // Lot Tetap per Posisi (Model 4 membuka 2 posisi)
extern double   MaxSpreadPoints             = 35.0;             // Maksimal Spread (Points/Cents pada Gold)

extern string   ---_INDICATOR_SETTINGS_---  = "=== INDIKATOR & FILTER ===";
extern int      H1_EMA_Fast                 = 50;               // Fast EMA di H1
extern int      H1_EMA_Slow                 = 200;              // Slow EMA di H1
extern int      M5_ATR_Period               = 14;               // Periode ATR di M5
extern double   M5_ATR_Multiplier_SL        = 1.0;              // Pengali ATR untuk Jarak Stop Loss
extern double   MaxCandleATRRatio           = 2.0;              // Filter Lilin Abnormal (>2.0x ATR = BATAL)

extern string   ---_TRADE_MANAGEMENT_---    = "=== MODEL 4 TRADE MANAGEMENT ===";
extern double   TP1_RR_Ratio                = 1.0;              // Target Posisi A (1R)
extern double   TP2_RR_Ratio                = 3.0;              // Target Posisi B (3R Runner)
extern bool     AutoMoveBEP_On_TP1          = true;             // Geser SL Posisi B ke BEP saat Posisi A Hit TP

extern string   ---_EA_SYSTEM_SETTINGS_---  = "=== SYSTEM CONFIG ===";
extern int      MagicNumber_PosA            = 777101;           // Magic Number Posisi A (TP1)
extern int      MagicNumber_PosB            = 777102;           // Magic Number Posisi B (TP2)
extern string   TradeComment                = "FS_M5_Model4";

//--- GLOBAL VARIABLES ---
datetime lastBarTime = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("Forex Sarjana M5 Scalper EA Berhasil Diinisialisasi!");
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("Forex Sarjana M5 Scalper EA Dimatikan.");
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   // 1. Kelola Posisi Aktif (Model 4: Auto BEP jika Posisi A sudah Close TP)
   if(AutoMoveBEP_On_TP1)
   {
      ManageModel4TrailingBEP();
   }

   // 2. Hanya eksekusi sinyal baru saat pembukaan Bar M5 baru
   if(Time[0] == lastBarTime) return;
   
   // 3. Filter Spread
   double currentSpread = (Ask - Bid) / Point;
   if(currentSpread > MaxSpreadPoints)
   {
      return;
   }

   // 4. Ambil Indikator H1 (Trend Filter)
   double h1_ema50  = iMA(Symbol(), PERIOD_H1, H1_EMA_Fast, 0, MODE_EMA, PRICE_CLOSE, 1);
   double h1_ema200 = iMA(Symbol(), PERIOD_H1, H1_EMA_Slow, 0, MODE_EMA, PRICE_CLOSE, 1);
   
   bool isH1Uptrend   = (h1_ema50 > h1_ema200);
   bool isH1Downtrend = (h1_ema50 < h1_ema200);

   // 5. Ambil Data Candlestick M5
   // Bar 1 = Candle Konfirmasi, Bar 2 = Candle Engulfing, Bar 3 = Candle Sebelum Engulfing
   double c1_open  = iOpen(Symbol(), PERIOD_M5, 1);
   double c1_close = iClose(Symbol(), PERIOD_M5, 1);
   double c1_high  = iHigh(Symbol(), PERIOD_M5, 1);
   double c1_low   = iLow(Symbol(), PERIOD_M5, 1);
   
   double c2_open  = iOpen(Symbol(), PERIOD_M5, 2);
   double c2_close = iClose(Symbol(), PERIOD_M5, 2);
   double c2_high  = iHigh(Symbol(), PERIOD_M5, 2);
   double c2_low   = iLow(Symbol(), PERIOD_M5, 2);

   double c3_open  = iOpen(Symbol(), PERIOD_M5, 3);
   double c3_close = iClose(Symbol(), PERIOD_M5, 3);

   double m5_atr = iATR(Symbol(), PERIOD_M5, M5_ATR_Period, 1);

   // 6. Filter Lilin Abnormal (> MaxCandleATRRatio x ATR)
   double c1_range = c1_high - c1_low;
   double c2_range = c2_high - c2_low;
   if(c1_range > (MaxCandleATRRatio * m5_atr) || c2_range > (MaxCandleATRRatio * m5_atr))
   {
      // Abaikan sinyal abnormal candle sesuai aturan Forex Sarjana
      lastBarTime = Time[0];
      return;
   }

   // 7. Cek Apakah Sudah Ada Posisi Terbuka untuk Simbol ini
   if(CountOpenOrders() > 0) return;

   // 8. Logika BUY: H1 Uptrend + M5 Bullish Engulfing + Candle Konfirmasi Hijau
   bool isBullishEngulfing = (c3_close < c3_open) && (c2_close > c2_open) && (c2_open <= c3_close) && (c2_close >= c3_open);
   bool isGreenConfirmation = (c1_close > c1_open) && (c1_close > c2_close);

   if(isH1Uptrend && isBullishEngulfing && isGreenConfirmation)
   {
      double swingLow = MathMin(c1_low, MathMin(c2_low, iLow(Symbol(), PERIOD_M5, 3)));
      double slPrice  = swingLow - (M5_ATR_Multiplier_SL * m5_atr);
      double riskDist = Ask - slPrice;

      if(riskDist > 0)
      {
         double tp1Price = Ask + (TP1_RR_Ratio * riskDist);
         double tp2Price = Ask + (TP2_RR_Ratio * riskDist);
         double lotSize  = CalculateLotSize(riskDist);

         // Buka 2 Posisi Split (Model 4)
         int ticketA = OrderSend(Symbol(), OP_BUY, lotSize, Ask, 3, slPrice, tp1Price, TradeComment + "_A", MagicNumber_PosA, 0, clrBlue);
         int ticketB = OrderSend(Symbol(), OP_BUY, lotSize, Ask, 3, slPrice, tp2Price, TradeComment + "_B", MagicNumber_PosB, 0, clrGreen);

         if(ticketA > 0 && ticketB > 0)
         {
            Print("BUY Setup Model 4 Berhasil Dieksekusi! Ticket A: ", ticketA, " | Ticket B: ", ticketB);
            lastBarTime = Time[0];
         }
      }
   }

   // 9. Logika SELL: H1 Downtrend + M5 Bearish Engulfing + Candle Konfirmasi Merah
   bool isBearishEngulfing = (c3_close > c3_open) && (c2_close < c2_open) && (c2_open >= c3_close) && (c2_close <= c3_open);
   bool isRedConfirmation = (c1_close < c1_open) && (c1_close < c2_close);

   if(isH1Downtrend && isBearishEngulfing && isRedConfirmation)
   {
      double swingHigh = MathMax(c1_high, MathMax(c2_high, iHigh(Symbol(), PERIOD_M5, 3)));
      double slPrice   = swingHigh + (M5_ATR_Multiplier_SL * m5_atr) + ((Ask - Bid));
      double riskDist  = slPrice - Bid;

      if(riskDist > 0)
      {
         double tp1Price = Bid - (TP1_RR_Ratio * riskDist);
         double tp2Price = Bid - (TP2_RR_Ratio * riskDist);
         double lotSize  = CalculateLotSize(riskDist);

         // Buka 2 Posisi Split (Model 4)
         int ticketA = OrderSend(Symbol(), OP_SELL, lotSize, Bid, 3, slPrice, tp1Price, TradeComment + "_A", MagicNumber_PosA, 0, clrRed);
         int ticketB = OrderSend(Symbol(), OP_SELL, lotSize, Bid, 3, slPrice, tp2Price, TradeComment + "_B", MagicNumber_PosB, 0, clrOrange);

         if(ticketA > 0 && ticketB > 0)
         {
            Print("SELL Setup Model 4 Berhasil Dieksekusi! Ticket A: ", ticketA, " | Ticket B: ", ticketB);
            lastBarTime = Time[0];
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Model 4 Trade Management: Geser SL Posisi B ke BEP saat Pos A TP |
//+------------------------------------------------------------------+
void ManageModel4TrailingBEP()
{
   bool hasPosA = false;
   int ticketPosB = -1;
   double openPriceB = 0;
   double currentSL_B = 0;
   int orderTypeB = -1;

   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderSymbol() == Symbol())
         {
            if(OrderMagicNumber() == MagicNumber_PosA)
            {
               hasPosA = true;
            }
            else if(OrderMagicNumber() == MagicNumber_PosB)
            {
               ticketPosB  = OrderTicket();
               openPriceB  = OrderOpenPrice();
               currentSL_B = OrderStopLoss();
               orderTypeB  = OrderType();
            }
         }
      }
   }

   // Jika Posisi A sudah TIDAK ADA (artinya sudah Take Profit 1R),
   // dan Posisi B masih aktif dengan SL belum di BEP:
   if(!hasPosA && ticketPosB > 0)
   {
      if(orderTypeB == OP_BUY)
      {
         if(currentSL_B < openPriceB) // Belum di BEP
         {
            bool res = OrderModify(ticketPosB, openPriceB, openPriceB, OrderTakeProfit(), 0, clrGold);
            if(res) Print("Posisi A TP Tercapai -> Stop Loss Posisi B Berhasil Digeser ke BEP (", openPriceB, ")");
         }
      }
      else if(orderTypeB == OP_SELL)
      {
         if(currentSL_B > openPriceB || currentSL_B == 0) // Belum di BEP
         {
            bool res = OrderModify(ticketPosB, openPriceB, openPriceB, OrderTakeProfit(), 0, clrGold);
            if(res) Print("Posisi A TP Tercapai -> Stop Loss Posisi B Berhasil Digeser ke BEP (", openPriceB, ")");
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Hitung Lot Size (Fixed atau Auto Risk %)                          |
//+------------------------------------------------------------------+
double CalculateLotSize(double riskDistance)
{
   if(!UseAutoLot) return FixedLotPerPosition;

   double riskAmount = AccountBalance() * (RiskPercentPerTrade / 100.0) / 2.0; // dibagi 2 untuk posisi A & B
   double tickValue  = MarketInfo(Symbol(), MODE_TICKVALUE);
   double tickSize   = MarketInfo(Symbol(), MODE_TICKSIZE);
   
   if(tickSize == 0 || tickValue == 0 || riskDistance == 0) return FixedLotPerPosition;

   double lotStep = MarketInfo(Symbol(), MODE_LOTSTEP);
   double minLot  = MarketInfo(Symbol(), MODE_MINLOT);
   double maxLot  = MarketInfo(Symbol(), MODE_MAXLOT);

   double rawLot = (riskAmount / (riskDistance / tickSize * tickValue));
   double normalizedLot = MathFloor(rawLot / lotStep) * lotStep;

   if(normalizedLot < minLot) normalizedLot = minLot;
   if(normalizedLot > maxLot) normalizedLot = maxLot;

   return normalizedLot;
}

//+------------------------------------------------------------------+
//| Hitung Total Order Terbuka EA Ini                                |
//+------------------------------------------------------------------+
int CountOpenOrders()
{
   int count = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderSymbol() == Symbol() && (OrderMagicNumber() == MagicNumber_PosA || OrderMagicNumber() == MagicNumber_PosB))
         {
            count++;
         }
      }
   }
   return count;
}
