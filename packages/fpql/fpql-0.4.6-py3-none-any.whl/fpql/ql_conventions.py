#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import QuantLib as ql
from QuantLib.QuantLib import ZARCurrency

"""
Created on Tue Jul  18 17:33:15 2021

@author: RMS671214
"""

ql_day_count = {
    'Actual/365 Fixed': ql.Actual365Fixed(), 
    'Actual/365 Fixed (Canadian)': ql.Actual365Fixed(ql.Actual365Fixed.Canadian), 
    'Actual/365 Fixed (No Leap)': ql.Actual365Fixed(ql.Actual365Fixed.NoLeap),
    'Actual/360': ql.Actual360(),
    'Actual/Actual': ql.ActualActual(),
    'Actual/Actual (ISMA)':ql.ActualActual(ql.ActualActual.ISMA),
    'Actual/Actual (Bond)':ql.ActualActual(ql.ActualActual.Bond),
    'Actual/Actual (ISDA)':ql.ActualActual(ql.ActualActual.ISDA),
    'Actual/Actual (Historical)':ql.ActualActual(ql.ActualActual.Historical),
    'Actual/Actual (Actual365)':ql.ActualActual(ql.ActualActual.Actual365),
    'Actual/Actual (AFB)':ql.ActualActual(ql.ActualActual.AFB),
    'Business252':ql.Business252(),
    'Thirty360': ql.Thirty360()
}  

ql_business_day = {
    "No Adjustment": ql.Unadjusted, 
    "Following": ql.Following, 
    "Modified Following": ql.ModifiedFollowing,
    "Preceding": ql.Preceding, 
    "Modified Preceding": ql.ModifiedPreceding
}

ql_date_generation = {
    "Forward from issue date": ql.DateGeneration.Forward,
    "Backward from maturity date": ql.DateGeneration.Backward,
    "Zero": ql.DateGeneration.Zero,
    "ThirdWednesday": ql.DateGeneration.ThirdWednesday,
    "Twentieth": ql.DateGeneration.Twentieth,
    "TwentiethIMM": ql.DateGeneration.TwentiethIMM,
    "CDS": ql.DateGeneration.CDS,
}

ql_frequency = {
    "No Frequency": ql.NoFrequency,
    "Once": ql.Once,
    "Annual": ql.Annual, 
    "Semi-Annual": ql.Semiannual, 
    "Every Four Months": ql.EveryFourthMonth,
    "Quarterly": ql.Quarterly,
    "Bi-Monthly": ql.Bimonthly,
    "Monthly": ql.Monthly,
    "Every Fourth Week": ql.EveryFourthWeek,
    "Bi-Weekly": ql.Biweekly,
    "Weekly": ql.Weekly,
    "Daily": ql.Daily
}

ql_freq_tenor = {
    "Annual": "1Y",
    "Semi-Annual": "6M",
    "Every Four Months": "4M",
    "Quarterly": "3M",
    "Bi-Monthly": "2M",
    "Monthly": "1M",
    "Every Fourth Week": "4W",
    "Bi-Weekly": "2W",
    "Weekly": "1W",
    "Daily": "1D"
}

ql_tenor = {
    "M": ql.Months,
    "Y": ql.Years,
    "W": ql.Weeks,
    "D": ql.Days
}

ql_compounding = {
    "Simple": ql.Simple,
    "Compounded": ql.Compounded,
    "Continuous": ql.Continuous,
    "SimpleThenCompounded": ql.SimpleThenCompounded,
    "CompoundedThenSimple": ql.CompoundedThenSimple
}

ql_calendar_market = {
    "Argentina": ql.Argentina(),
    "Argentina (Merval)": ql.Argentina(ql.Argentina.Merval),
    "Brazil" : ql.Brazil(),
    "Brazil (Exchange)" : ql.Brazil(ql.Brazil.Exchange),
    "Brazil (Settlement)" : ql.Brazil(ql.Brazil.Settlement),
    "Canada": ql.Canada(),
    "Canada (Settlement)": ql.Canada(ql.Canada.Settlement),
    "Canada (TSX)": ql.Canada(ql.Canada.TSX),
    "China": ql.China(),
    "China (IB)": ql.China(ql.China.IB),
    "China (SSE)": ql.China(ql.China.SSE),
    "Czech Republic" : ql.CzechRepublic(),
    "Czech Republic (PSE)" : ql.CzechRepublic(ql.CzechRepublic.PSE),
    "France" : ql.France(),
    "France (Exchange)" : ql.France(ql.France.Exchange),
    "France (Settlement)" : ql.France(ql.France.Settlement),
    "Germany" : ql.Germany(),
    "Germany (Eurex)": ql.Germany(ql.Germany.Eurex),
    "Germany (FrankfurtStockExchange)": ql.Germany(ql.Germany.FrankfurtStockExchange), 
    "Germany (Settlement)": ql.Germany(ql.Germany.Settlement),
    "Germany (Xetra)": ql.Germany(ql.Germany.Xetra),
    "Hong Kong": ql.HongKong(),
    "Hong Kong (HKEx)": ql.HongKong(ql.HongKong.HKEx),
    "Iceland": ql.Iceland(),
    "Iceland (ICEX)" : ql.Iceland(ql.Iceland.ICEX),
    "India" : ql.India(),
    "India (NSE)": ql.India(ql.India.NSE),
    "Indonesia" : ql.Indonesia(),
    "Indonesia (BEJ)": ql.Indonesia(ql.Indonesia.BEJ),
    "Indonesia (JSX)": ql.Indonesia(ql.Indonesia.JSX),
    "Israel": ql.Israel(),
    "Israel (Settlement)": ql.Israel(ql.Israel.Settlement),
    "Israel (TASE)": ql.Israel(ql.Israel.TASE),
    "Italy": ql.Italy(),
    "Italy (Exchange)": ql.Italy(ql.Italy.Exchange),
    "Italy (Settlement)": ql.Italy(ql.Italy.Settlement),
    "Mexico": ql.Mexico(),
    "Mexico (BMV)": ql.Mexico(ql.Mexico.BMV),
    "Russia": ql.Russia(),
    "Russia (MOEX)": ql.Russia(ql.Russia.MOEX),
    "Russia (Settlement)": ql.Russia(ql.Russia.Settlement),
    "Saudi Arabia": ql.SaudiArabia(),
    "Saudi Arabia (Tadawul)": ql.SaudiArabia(ql.SaudiArabia.Tadawul),
    "Singapore": ql.Singapore(),
    "Singapore (SGX)": ql.Singapore(ql.Singapore.SGX),
    "Slovakia": ql.Slovakia(),
    "Slovakia (BSSE)": ql.Slovakia(ql.Slovakia.BSSE),
    "South Korea": ql.SouthKorea(),
    "South Korea (KRX)": ql.SouthKorea(ql.SouthKorea.KRX),
    "South Korea (Settlement)": ql.SouthKorea(ql.SouthKorea.Settlement),
    "Taiwan": ql.Taiwan(),
    "Taiwan (TSEC)": ql.Taiwan(ql.Taiwan.TSEC),
    "Ukraine" : ql.Ukraine(),
    "Ukraine (USE)": ql.Ukraine(ql.Ukraine.USE),
    "United Kingdom" : ql.UnitedKingdom(),
    "United Kingdom (Exchange)": ql.UnitedKingdom(ql.UnitedKingdom.Exchange),
    "United Kingdom (Metals)": ql.UnitedKingdom(ql.UnitedKingdom.Metals),
    "United Kingdom (Settlement)": ql.UnitedKingdom(ql.UnitedKingdom.Settlement),
    "United States": ql.UnitedStates(),
    "United States (FederalReserve)": ql.UnitedStates(ql.UnitedStates.FederalReserve),
    "United States (GovernmentBond)": ql.UnitedStates(ql.UnitedStates.GovernmentBond),
    "United States (LiborImpact)": ql.UnitedStates(ql.UnitedStates.LiborImpact),
    "United States (NREC)": ql.UnitedStates(ql.UnitedStates.NERC),
    "United States (NYSE)": ql.UnitedStates(ql.UnitedStates.NYSE),
    "United States (Settlement)": ql.UnitedStates(ql.UnitedStates.Settlement) ,
    "TARGET": ql.TARGET(),
    "WeekendsOnly": ql.WeekendsOnly(),
    "NullCalendar": ql.NullCalendar()
}

ql_start_basis = { "Today": 0, "Tom": 1, "Spot": 2}


irmodels = ['Vasicek', 'BlackKarasinski', 'HullWhite', "gsr", 'g2']


ql_ccy = [{"code": "ZAR", "description": "South-AFrican Rand", "ql": ql.ZARCurrency()}, 
            {"code": "ARS", "description": "Argentinian Peso", "ql": ql.ARSCurrency()}, 
            {"code": "BRL", "description": "Brazilian Real", "ql": ql.BRLCurrency()}, 
            {"code": "CAD", "description": "Canadian Dollar", "ql": ql.CADCurrency()}, 
            {"code": "CLP", "description": "Chilean Peso", "ql": ql.CLPCurrency()}, 
            {"code": "COP", "description": "Colombian Peso", "ql": ql.COPCurrency()}, 
            {"code": "MXN", "description": "Mexican Peso", "ql": ql.MXNCurrency()}, 
            {"code": "PEH", "description": "Peruvian Sol", "ql": ql.PEHCurrency()}, 
            {"code": "PEI", "description": "Peruvian Inti", "ql": ql.PEICurrency()}, 
            {"code": "PEN", "description": "Peruvian Nuevo Sol", "ql": ql.PENCurrency()}, 
            {"code": "TTD", "description": "Trinidad & Tobago Dollar", "ql": ql.TTDCurrency()}, 
            {"code": "USD", "description": "US Dollar", "ql": ql.USDCurrency()}, 
            {"code": "VEB", "description": "Venezuelan Bolivar", "ql": ql.VEBCurrency()}, 
            {"code": "BDT", "description": "Bangladesh Taka", "ql": ql.BDTCurrency()}, 
            {"code": "CNY", "description": "Chinese Yuan", "ql": ql.CNYCurrency()}, 
            {"code": "HKD", "description": "Hong Kong Dollar", "ql": ql.HKDCurrency()}, 
            {"code": "ILS", "description": "Israeli Shekel", "ql": ql.ILSCurrency()}, 
            {"code": "INR", "description": "Indian Rupee", "ql": ql.INRCurrency()}, 
            {"code": "IQD", "description": "Iraqi Dinar", "ql": ql.IQDCurrency()}, 
            {"code": "IRR", "description": "Iranian Rial", "ql": ql.IRRCurrency()}, 
            {"code": "JPY", "description": "Japanese Yen", "ql": ql.JPYCurrency()}, 
            {"code": "KRW", "description": "South Korean Won", "ql": ql.KRWCurrency()}, 
            {"code": "KWD", "description": "Kuwaiti Dinar", "ql": ql.KWDCurrency()}, 
            {"code": "NPR", "description": "Nepal Rupee", "ql": ql.NPRCurrency()}, 
            {"code": "PKR", "description": "Pakistani Rupee", "ql": ql.PKRCurrency()}, 
            {"code": "SAR", "description": "Saudi Riyal", "ql": ql.SARCurrency()},
            {"code": "SGD", "description": "Singapore Dollar", "ql": ql.SGDCurrency()},
            {"code": "THB", "description": "Thai Baht", "ql": ql.THBCurrency()}, 
            {"code": "TWD", "description": "Taiwan Dollar", "ql": ql.TWDCurrency()}, 
            {"code": "ATS", "description": "Austrian Shilling", "ql": ql.ATSCurrency()}, 
            {"code": "BEF", "description": "Belgian Frn", "ql": ql.BEFCurrency()}, 
            {"code": "BGL", "description": "Bulgarian Ruble", "ql": ql.BGLCurrency()}, 
            {"code": "BYR", "description": "Belarussian Ruble", "ql": ql.BYRCurrency()}, 
            {"code": "CHF", "description": "Swiss Franc", "ql": ql.CHFCurrency()}, 
            {"code": "CYP", "description": "Cyprus Pound", "ql": ql.CYPCurrency()}, 
            {"code": "CZK", "description": "Czech Koruna", "ql": ql.CZKCurrency()},
            {"code": "DEM", "description": "Deutsche Mark", "ql": ql.DEMCurrency()}, 
            {"code": "DKK", "description": "Danish Krone", "ql": ql.ARSCurrency()}, 
            {"code": "EEK", "description": "Estonian Kroon", "ql": ql.EEKCurrency()},
            {"code": "ESP", "description": "Spanish Peseta", "ql": ql.ESPCurrency()}, 
            {"code": "EUR", "description": "European Euro", "ql": ql.EURCurrency()}, 
            {"code": "FIM", "description": "Finnish Markka", "ql": ql.FIMCurrency()}, 
            {"code": "FRF", "description": "French Franc", "ql": ql.FRFCurrency()}, 
            {"code": "GBP", "description": "Great Britain Pound", "ql": ql.GBPCurrency()}, 
            {"code": "GRD", "description": "Greek Drachma", "ql": ql.GRDCurrency()}, 
            {"code": "IDR", "description": "Indonesian Rupiah", "ql": ql.IDRCurrency()}, 
            {"code": "HUF", "description": "Hungarian Forint", "ql": ql.HUFCurrency()}, 
            {"code": "IEP", "description": "Irish Punt", "ql": ql.IEPCurrency()}, 
            {"code": "ISK", "description": "Iceland Krona", "ql": ql.ISKCurrency()}, 
            {"code": "ITL", "description": "Italian Lira", "ql": ql.ITLCurrency()}, 
            {"code": "LTL", "description": "Lithuanian Litas", "ql": ql.LTLCurrency()}, 
            {"code": "LUF", "description": "Luxemberg Fran", "ql": ql.LUFCurrency()}, 
            {"code": "LVL", "description": "Latvian Lat", "ql": ql.LVLCurrency()},
            {"code": "MTL", "description": "Maltese Lira", "ql": ql.MTLCurrency()},
            {"code": "NLG", "description": "Netherland Guilder", "ql": ql.NLGCurrency()}, 
            {"code": "NOK", "description": "Norwegian Krone", "ql": ql.NOKCurrency()}, 
            {"code": "PLN", "description": "Polish Zloty", "ql": ql.PLNCurrency()}, 
            {"code": "PTE", "description": "Portuguese Escudo", "ql": ql.PTECurrency()}, 
            {"code": "ROL", "description": "Romanian Leu", "ql": ql.ROLCurrency()}, 
            {"code": "RON", "description": "Romanian New Leu", "ql": ql.RONCurrency()}, 
            {"code": "SEK", "description": "Swedish Krona", "ql": ql.SEKCurrency()},
            {"code": "SIT", "description": "Slovenian Tolar", "ql": ql.SITCurrency()},
            {"code": "SKK", "description": "Slovak Koruna", "ql": ql.SKKCurrency()},
            {"code": "TRY", "description": "Turkish Lira", "ql": ql.TRYCurrency()},
            {"code": "AUD", "description": "Australian Dollar", "ql": ql.AUDCurrency()},
            {"code": "NZD", "description": "New Zealand Dollar", "ql": ql.NZDCurrency()},
            {"code": "MYR", "description": "Malaysian Ringgit", "ql": ql.MYRCurrency()},]