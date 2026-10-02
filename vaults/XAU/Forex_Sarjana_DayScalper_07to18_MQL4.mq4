//+------------------------------------------------------------------+
//|               Forex_Sarjana_DayScalper_07to18.mq4                |
//|               Hermes AI Agent - Professional Trader Engine       |
//|      Specialized Day-Scalper (07.00 - 18.00 WIB | Lot 0.01 Fixed)|
//+------------------------------------------------------------------+
#property copyright "Forex Sarjana & Hermes Agent"
#property link      "https://github.com/ahmdd4vd/apos"
#property version   "2.00"
#property strict

//--- INPUT PARAMETERS ---
extern string   ---_TIME_SETTINGS_---       = "=== JAM OPERASIONAL (WIB / UTC+7) ===";
extern int      BrokerGMTOffset             = 2;                // GMT Offset Broker (Standar Broker: GMT+2 atau GMT+3)
extern int      StartHourWIB                = 7;                // Jam Mulai Aktif (07.00 WIB)
extern int      EndHourWIB                  = 18;               // Jam Berhenti Entry Baru (18.00 WIB)
extern bool     CloseAllAtEndHour           = false;            // Tutup Paksa Semua Posisi pada Jam 18.00 WIB

extern string   ---_RISK_SETTINGS_---       = "=== RISK & MONEY MANAGEMENT ===";
extern double   FixedLotPerPosition         = 0.01;             // Lot Tetap 0.01 (Membuka 2 Split Posisi = 0.02 Lot)
extern double   MaxSpreadPoints             = 30.0;             // Maksimal Toleransi Spread (Points)

extern string   ---_STRATEGY_SETTINGS_---   = "=== STRATEGI & FILTER ===";
extern int      H1_EMA_Fast                 = 50;               // Fast EMA H1
extern int      H1_EMA_Slow                 = 200;              // Slow EMA H1
extern int      M5_ATR_Period               = 14;               // ATR Periode M5
extern double   M5_ATR_Multiplier_SL        = 1.0;              // Buffer SL Dinamis (1.0 x ATR)
extern double   MaxCandleATRRatio           = 2.0;              // Filter Lilin Abnormal (>2.0x ATR = Batal)

extern string   ---_MODEL_4_SETTINGS_---    = "=== MODEL 4 TRADE MANAGEMENT ===";
extern double   TP1_RR_Ratio                = 1.0;              // Target Posisi A (1R)
extern double   TP2_RR_Ratio                = 3.0;              // Target Posisi B (3R Runner)
extern bool     AutoMoveBEP_On_TP1          = true;             // Geser SL Posisi B ke BEP saat Pos A TP

extern string   ---_SYSTEM_CONFIG_---       = "=== SYSTEM CONFIG ===";
extern int      MagicNumber_PosA            = 999101;           // Magic Number Posisi A
extern int      MagicNumber_PosB            = 999102;           // Magic Number Posisi B
extern string   TradeComment                = "FS_Day_07to18";

//--- GLOBAL VARIABLES ---
datetime lastBarTime = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("EA Forex Sarjana Day-Scalper (07.00 - 18.00 WIB | Lot 0.01) Berhasil Diaktifkan!");
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("EA Forex Sarjana Day-Scalper Dinonaktifkan.");
}

//+------------------------------------------------------------------+
//| Konversi Waktu Broker ke Waktu Indonesia Barat (WIB / UTC+7)     |
//+------------------------------------------------------------------+
int GetCurrentWIBHour()
{
   datetime serverTime = TimeCurrent();
   int serverHour = TimeHour(serverTime);
   // ServerHour - BrokerGMTOffset = UTC Time
   // UTC Time + 7 = WIB Time
   int wibHour = (serverHour - BrokerGMTOffset + 7) % 24;
   if(wibHour < 0) wibHour += 24;
   return wibHour;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   int currentWIB = GetCurrentWIBHour();

   // 1. Kelola Posisi Aktif (Model 4: Auto BEP jika Posisi A sudah TP)
   if(AutoMoveBEP_On_TP1)
   {
      ManageModel4TrailingBEP();
   }

   // 2. Jika sudah jam 18.00 WIB dan opsi CloseAllAtEndHour aktif
   if(CloseAllAtEndHour && currentWIB >= EndHourWIB)
   {
      CloseAllPositions();
      return;
   }

   // 3. Filter Jam Operasional: Hanya entri antara jam 07.00 s/d 18.00 WIB
   if(currentWIB < StartHourWIB || currentWIB >= EndHourWIB)
   {
      return; // Di luar jam kerja, jangan buka posisi baru
   }

   // 4. Hanya eksekusi pada pembukaan bar M5 baru
   if(Time[0] == lastBarTime) return;

   // 5. Filter Spread
   double currentSpread = (Ask - Bid) / Point;
   if(currentSpread > MaxSpreadPoints) return;

   // 6. Baca Indikator Tren H1 (EMA 50 vs EMA 200)
   double h1_ema50  = iMA(Symbol(), PERIOD_H1, H1_EMA_Fast, 0, MODE_EMA, PRICE_CLOSE, 1);
   double h1_ema200 = iMA(Symbol(), PERIOD_H1, H1_EMA_Slow, 0, MODE_EMA, PRICE_CLOSE, 1);

   bool isH1Uptrend   = (h1_ema50 > h1_ema200);
   bool isH1Downtrend = (h1_ema50 < h1_ema200);

   // 7. Baca Candlestick M5 (Bar 1, Bar 2, Bar 3)
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

   // 8. Filter Lilin Abnormal
   double c1_range = c1_high - c1_low;
   double c2_range = c2_high - c2_low;
   if(c1_range > (MaxCandleATRRatio * m5_atr) || c2_range > (MaxCandleATRRatio * m5_atr))
   {
      lastBarTime = Time[0];
      return;
   }

   // 9. Cek Apakah Sudah Ada Posisi Terbuka
   if(CountOpenOrders() > 0) return;

   // 10. SETUP BUY
   bool isBullishEngulfing = (c3_close < c3_open) && (c2_close > c2_open) && (c2_open <= c3_close) && (c2_close >= c3_open);
   bool isGreenConfirmation = (c1_close > c1_open) && (c1_close > c2_close);

   if(isH1Uptrend && isBullishEngulfing && isGreenConfirmation)
   {
      double swingLow = MathMin(c1_low, MathMin(c2_low, iLow(Symbol(), PERIOD_M5, 3)));
      double slPrice  = swingLow - (M5_ATR_Multiplier_SL * m5_atr);
      double riskDist = Ask - slPrice;

      if(riskDist > 0.40)
      {
         double tp1Price = Ask + (TP1_RR_Ratio * riskDist);
         double tp2Price = Ask + (TP2_RR_Ratio * riskDist);

         int ticketA = OrderSend(Symbol(), OP_BUY, FixedLotPerPosition, Ask, 3, slPrice, tp1Price, TradeComment + "_A", MagicNumber_PosA, 0, clrBlue);
         int ticketB = OrderSend(Symbol(), OP_BUY, FixedLotPerPosition, Ask, 3, slPrice, tp2Price, TradeComment + "_B", MagicNumber_PosB, 0, clrGreen);

         if(ticketA > 0 && ticketB > 0)
         {
            Print("[07-18 WIB] BUY Setup Model 4 Berhasil Dieksekusi (Lot 0.01 x 2)!");
            lastBarTime = Time[0];
         }
      }
   }

   // 11. SETUP SELL
   bool isBearishEngulfing = (c3_close > c3_open) && (c2_close < c2_open) && (c2_open >= c3_close) && (c2_close <= c3_open);
   bool isRedConfirmation = (c1_close < c1_open) && (c1_close < c2_close);

   if(isH1Downtrend && isBearishEngulfing && isRedConfirmation)
   {
      double swingHigh = MathMax(c1_high, MathMax(c2_high, iHigh(Symbol(), PERIOD_M5, 3)));
      double slPrice   = swingHigh + (M5_ATR_Multiplier_SL * m5_atr) + ((Ask - Bid));
      double riskDist  = slPrice - Bid;

      if(riskDist > 0.40)
      {
         double tp1Price = Bid - (TP1_RR_Ratio * riskDist);
         double tp2Price = Bid - (TP2_RR_Ratio * riskDist);

         int ticketA = OrderSend(Symbol(), OP_SELL, FixedLotPerPosition, Bid, 3, slPrice, tp1Price, TradeComment + "_A", MagicNumber_PosA, 0, clrRed);
         int ticketB = OrderSend(Symbol(), OP_SELL, FixedLotPerPosition, Bid, 3, slPrice, tp2Price, TradeComment + "_B", MagicNumber_PosB, 0, clrOrange);

         if(ticketA > 0 && ticketB > 0)
         {
            Print("[07-18 WIB] SELL Setup Model 4 Berhasil Dieksekusi (Lot 0.01 x 2)!");
            lastBarTime = Time[0];
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Model 4 Auto-BEP Management                                      |
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
            if(OrderMagicNumber() == MagicNumber_PosA) hasPosA = true;
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

   if(!hasPosA && ticketPosB > 0)
   {
      if(orderTypeB == OP_BUY && currentSL_B < openPriceB)
      {
         OrderModify(ticketPosB, openPriceB, openPriceB, OrderTakeProfit(), 0, clrGold);
      }
      else if(orderTypeB == OP_SELL && (currentSL_B > openPriceB || currentSL_B == 0))
      {
         OrderModify(ticketPosB, openPriceB, openPriceB, OrderTakeProfit(), 0, clrGold);
      }
   }
}

//+------------------------------------------------------------------+
//| Tutup Semua Posisi Jam 18.00 WIB                                 |
//+------------------------------------------------------------------+
void CloseAllPositions()
{
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
      {
         if(OrderSymbol() == Symbol() && (OrderMagicNumber() == MagicNumber_PosA || OrderMagicNumber() == MagicNumber_PosB))
         {
            if(OrderType() == OP_BUY) OrderClose(OrderTicket(), OrderLots(), Bid, 3, clrGray);
            else if(OrderType() == OP_SELL) OrderClose(OrderTicket(), OrderLots(), Ask, 3, clrGray);
         }
      }
   }
}

//+------------------------------------------------------------------+
//| Hitung Total Order Aktif EA                                      |
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
