import QuantLib as ql
from numpy import datetime64 as dt64, datetime_as_string as datestr
from typing import List
from . import pymodels, ql_enums as qle, ql_utils as qlu, \
    ql_conventions as qlc, bonds, termstructure as ts


class FixedBondVal:
    def __init__(self):
        pass

    @property
    def bond_info(self):
        return self.__bond_info

    @bond_info.setter
    def bond_info(self, bond_info):
        self.__bond_info = bond_info


class FixedRateBond:
    def __init__(self, date: str, fixbond: pymodels.FixedRateBond, qlcalendar=None):
        self.__fixbond = fixbond
        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()   
        
        self.__sys_date = ql.Settings.instance().evaluationDate
        ql.Settings.instance().evaluationDate = ql.Date(date,'%Y-%m-%d')
        structures = bonds.calc_fixbond_structures(date, self.__fixbond, 
                                                    self.__fixbond.settings, 
                                                    self.__qlcalendar)
        self.__fixbond.structure = structures

    
    def stats(self, clean_price: float=None, bond_yield: float=None, 
                curve: ql.QuantLib.YieldTermStructure = None,
                spreads: List[pymodels.Rate] = None): 

        vdate = ql.Settings.instance().evaluationDate
        setting = self.__fixbond.settings
        qlfixratebond = bonds.get_qlfixedratebond(self.__fixbond, setting, self.__qlcalendar)

        if clean_price or bond_yield:
            if clean_price:
                clean_price = float(clean_price)
                ytm = bonds.fixbond_ytm(clean_price, 
                                        setting.day_count, 
                                        setting.frequency, 
                                        qlfixratebond)
            else:
                ytm = bond_yield
        
            ql_ir = ql.InterestRate(float(ytm)/100, 
                                qlc.ql_day_count[setting.day_count], 
                                ql.Compounded, 
                                qlc.ql_frequency[setting.frequency])
            
            risks = bonds.bond_functions_risks(qlfixratebond, ql_ir)
            risks.ytm = ytm
            return risks

        elif curve:
            curve_handle = ql.YieldTermStructureHandle(curve)
            curve_engine = ql.DiscountingBondEngine(curve_handle)
            qlfixratebond.setPricingEngine(curve_engine)
            value = qlfixratebond.NPV()
            accrued = qlfixratebond.accruedAmount()
            clean_price = value - accrued
            ytm  = qlfixratebond.bondYield(clean_price,
                                    qlc.ql_day_count[setting.day_count],
                                    ql.Compounded,
                                    qlc.ql_frequency[setting.frequency],
                                    vdate) * 100
            ql_ir = ql.InterestRate(float(ytm)/100, 
                                qlc.ql_day_count[setting.day_count], 
                                ql.Compounded, 
                                qlc.ql_frequency[setting.frequency])
            risks = bonds.bond_functions_risks(qlfixratebond, ql_ir)
            if spreads:
                spread_handle = ts.ql_spread_handle(vdate.ISO(),
                                    curve, 
                                    spreads)
                spread_engine = ql.DiscountingBondEngine(spread_handle)
                qlfixratebond.setPricingEngine(spread_engine)
                risks.value_after_shift = qlfixratebond.NPV()
            
                
            return risks



class ConvertibleFixedRateBond:
    def __init__(self, thebond: pymodels.ConvertibleFixedRate, qlcalendar):
        self.__convbond = thebond
        self.__engine = None
        self.__qlcalendar = qlcalendar
    
    @property
    def engine(self):
        return self.__engine

    @engine.setter
    def engine(self, engine):
        self.__engine = engine


    @property
    def thebond(self):
        return self.__convbond
    

    @property
    def qlcalendar(self):
        return self.__qlcalendar

    @qlcalendar.setter
    def qlcalendar(self, qlcalendar):
        self.qlcalendar = qlcalendar


    def qlconvertible(self, value_date:str):
        exercise = self.__exercise(value_date)
        dividend_schedule = self.__dividend_schedule_from_dividend_structure()
        callability_schedule = self.__call_schedule_from_option_schedules()
        credit_spread_handle = ql.QuoteHandle(ql.SimpleQuote(self.__convbond.credit_spread/100))
        #print(self.__convbond.structure)
        if self.__convbond.structure:
            #print(self.__convbond.structure)
            schedule = qlu.qlSchedule_from_Structure(self.__convbond.structure)
            convertible = ql.ConvertibleFixedCouponBond(exercise,
                                                    self.__convbond.conversion_ratio,
                                                    dividend_schedule,
                                                    callability_schedule, 
                                                    credit_spread_handle,
                                                    qlu.datestr_to_qldate(self.__convbond.issue_date),
                                                    0,
                                                    [self.__convbond.coupon/100],
                                                    qlc.ql_day_count[self.__convbond.settings.day_count],
                                                    schedule,
                                                    self.__convbond.redemption)
            return convertible
        else:
            return None


    def __exercise(self, value_date: str, ):
        
        if self.__convbond.exercise_type == qle.OptionExercise.american:
            vdate = qlu.datestr_to_qldate(value_date)
            mdate = qlu.datestr_to_qldate(self.__convbond.maturity)
            return ql.AmericanExercise(vdate, mdate)
        
        elif self.__convbond.exercise_type == qle.OptionExercise.bermudan:
            dates = []
            callschedule = self.__convbond.call_list
            putschedule = self.__convbond.put_list
            schedule = callschedule + putschedule
            sorted_schedule = sorted(schedule, key=lambda d: d.date)
            for sche in sorted_schedule:
                dates.append(qlu.datestr_to_qldate(sche.date))
            return ql.BermudanExercise(dates)
        else:
            edate = qlu.datestr_to_qldate(self.__convbond.european_expiry)
            return ql.EuropeanExercise(edate)


    def __call_schedule_from_option_schedules(self):
        callschedule = self.__convbond.call_list
        putschedule = self.__convbond.put_list
        schedule = callschedule + putschedule
        sorted_schedule = sorted(schedule, key=lambda d: d.date)
        #print(sorted_schedule)
        option_schedule = ql.CallabilitySchedule()
        for sche in sorted_schedule:
            option_price  = ql.CallabilityPrice(sche.price, 
                                                sche.price_type)
            optionality = ql.Callability(option_price, 
                                        sche.option_type,
                                        qlu.datestr_to_qldate(sche.date))
            option_schedule.append(optionality)
        return option_schedule
    

    def __dividend_schedule_from_dividend_structure(self):
        dividend_schedule = ql.DividendSchedule() # No dividends
        for cf in self.__convbond.dividend_structure:
            ql_fixeddividend = ql.FixedDividend(cf.amount, 
                                            qlu.datestr_to_qldate(cf.date))
            dividend_schedule.append(ql_fixeddividend)
        return dividend_schedule


    def create_dividend_structure_from_dividend_yield(self, 
                                                    value_date: str,
                                                    qlcalendar):
        self.__convbond.dividend_structure = []
        dividend_amount = 0.01 * self.__convbond.dividend_yield * \
                        self.__convbond.stock_price
        next_dividend_date = qlu.datestr_to_qldate(value_date)
        mdate = qlu.datestr_to_qldate(self.__convbond.maturity)

        while next_dividend_date < mdate:
            next_dividend_date = qlcalendar.advance(next_dividend_date, 1, ql.Years)
            cf = {"date": next_dividend_date.ISO(), "amount": dividend_amount}
            cf_class = pymodels.CashFlow(**cf)
            self.__convbond.dividend_structure.append(cf_class)
        #print(self.__convbond.dividend_structure)


    def create_coupon_structure_from_qlschedule(self):
        #downcast self__convbond to FixedRateBond class
        thedict = self.__convbond.dict(exclude={'redemption',
                                            'conversion_price',
                                            'conversion_ratio',
                                            'dividend_yield',
                                            'dividend_structure',
                                            'stock_price',
                                            'call_info',
                                            'put_info',
                                            'exercise_type',
                                            'european_expiry',
                                            'credit_spread'})
        thebond = pymodels.FixedRateBond(**thedict)
        qlSchedule = qlu.qlSchedule2(thebond, self.__qlcalendar)
        self.__convbond.structure = qlu.structure_from_qlSchedule(thebond, qlSchedule)


class FRAs:
    def __init__(self, fras: List[pymodels.FRA], setting: pymodels.DepoSetting,
                qlcalendar=None):
        self.__fras = fras
        self.__setting = setting
        #self.__current_date = current_date
        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()


    @property
    def qlcalendar(self):
        return self.__qlcalendar

    @qlcalendar.setter
    def qlcalendar(self, qlcalendar):
        self.__qlcalendar = qlcalendar

    
    def generate_dates(self):
        cal = self.__qlcalendar
        cdate = ql.Settings.instance().evaluationDate
        setting = self.__setting
        fras = self.__fras
        
        for fra in fras:
            #start date is not defined
            if not fra.start_date:
                # calculate the start date, then end date of the fra
                if fra.start_tenor:
                    qlperiod = ql.Period(fra.start_tenor)
                    business_day = qlc.ql_business_day[setting.business_day]
                    fra.start_date = cal.advance(cdate, qlperiod, business_day, False).ISO()
                    sdate = ql.Date(fra.start_date, '%Y-%m-%d')
                    if fra.end_tenor:
                        qlperiod = ql.Period(fra.end_tenor)
                        business_day = qlc.ql_business_day[setting.business_day]
                        fra.end_date = cal.advance(sdate, qlperiod, business_day, False).ISO()
                else:
                    fra.start_date = None
                    fra.end_date = None


    def helpers(self):
        frahelpers = []
        fras = self.__fras
        for fra in fras:
            start = ql.Period(fra.start_tenor).length()
            period = ql.Period(fra.depo.tenor).length()
            end = start + period
            setting = self.__setting
            business_day = qlc.ql_business_day[setting.business_day]
            day_count = qlc.ql_day_count[setting.day_count]
            quote = ql.QuoteHandle(ql.SimpleQuote(fra.depo.rate/100))
            helper =  ql.FraRateHelper(quote, 
                                    start, 
                                    end, 
                                    fra.depo.start_basis, 
                                    self.__qlcalendar, 
                                    business_day, 
                                    fra.eom, 
                                    day_count)
            frahelpers.append(helper)
        return frahelpers


class Deposits:
    def __init__(self, rates: List[pymodels.Rate], setting: pymodels.DepoSetting,
        qlcalendar=None):
        self.__rates = rates
        self.__setting = setting
        #self.__current_date = current_date
        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()    

    @property
    def rates(self):
        return self.__rates

    @rates.setter
    def rates(self, rates):
        self.__rates = rates


    @property
    def setting(self):
        return self.__setting

    @setting.setter
    def setting(self, setting):
        self.__setting = setting  

    def generate_dates(self):
        pass


    def helpers(self):
        setting = self.__setting
        rates = self.__rates
        business_day = qlc.ql_business_day[setting.business_day]
        day_count = qlc.ql_day_count[setting.day_count]
        depo_helpers = []

        for rate in rates:
            if rate.start_basis:
                start_basis = rate.start_basis
            else:
                start_basis = setting.start_basis
            
            if rate.eom:
                eom = rate.eom
            else:
                eom = setting.eom
            helper = ql.DepositRateHelper(rate.rate/100, 
                                        ql.Period(rate.tenor), 
                                        start_basis, 
                                        self.__qlcalendar, 
                                        business_day, 
                                        eom, 
                                        day_count)
            depo_helpers.append(helper)
        return depo_helpers


class ParBond:
    def __init__(self, rates: List[pymodels.Rate], setting: pymodels.BondSetting,
        qlcalendar=None):
        self.__rates = rates
        self.__setting = setting
        #self.__current_date = current_date
        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()  


    @property
    def rates(self):
        return self.__rates

    @rates.setter
    def rates(self, rates):
        self.__rates = rates


    @property
    def setting(self):
        return self.__setting

    @setting.setter
    def setting(self, setting):
        self.__setting = setting  


    def helpers(self):
        setting = self.__setting
        rates = self.__rates
        business_day = qlc.ql_business_day[setting.business_day]
        day_count = qlc.ql_day_count[setting.day_count]
        cal = self.__qlcalendar
        eom = setting.is_eom
        date_gen = qlc.ql_date_generation[setting.date_gen]
        ql_period = ql.Period(qlc.ql_freq_tenor[setting.frequency])

        if setting.terminate_business_day:
            t_bus_day = qlc.ql_business_day[setting.terminate_business_day]
        else:
            t_bus_day = qlc.ql_business_day[setting.business_day]

        quote_handle = ql.QuoteHandle(ql.SimpleQuote(100))
        par_helpers = []

        for rate in rates:
            #Need ql.Schedule to use ql.FixedRateBondHelper
            cdate = ql.Settings.instance().evaluationDate
            sdate = cal.advance(cdate, 
                                ql.Period(setting.start_basis, ql.Days),     
                                business_day, 
                                eom)
            maturity = cal.advance(sdate, ql.Period(rate.tenor),     
                                    business_day, 
                                    eom)
            schedule = ql.Schedule(sdate, 
                                maturity, 
                                ql_period, 
                                cal, 
                                business_day,
                                t_bus_day,
                                date_gen,
                                setting.is_eom)
        
            fix_helper = ql.FixedRateBondHelper(quote_handle, 
                                setting.start_basis, 
                                100, 
                                schedule, 
                                [rate.rate/100],
                                day_count)
            par_helpers.append(fix_helper)
        return par_helpers


class IBOR:
    def __init__(self, ibor: pymodels.IborFamily,
                qlcalendar=None, yts_handle=None):
        self.__ibor = ibor
        self.__name = ibor.name
        
        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()  
        
        indices = {}
        tenors = ibor.tenors
        business_day = qlc.ql_business_day[ibor.business_day]
        day_count = qlc.ql_day_count[ibor.day_count]
        currency =[ ccy for ccy in qlc.ql_ccy if ccy['code']==ibor.currency]
        if currency:
            ccy = currency[0]['ql']
        for tenor in tenors:
            if not yts_handle:
                indices[tenor] = ql.IborIndex(ibor.name, 
                                        ql.Period(tenor), 
                                        ibor.start_basis, 
                                        ccy, 
                                        self.__qlcalendar, 
                                        business_day, 
                                        ibor.eom, 
                                        day_count)
            else:
                indices[tenor] = ql.IborIndex(ibor.name, 
                                        ql.Period(tenor), 
                                        ibor.start_basis, 
                                        ccy, 
                                        self.__qlcalendar, 
                                        business_day, 
                                        ibor.eom, 
                                        day_count, 
                                        yts_handle)
        self.__indices = indices


    def getindex(self, tenor):
        return self.__indices.get(tenor)


class OIS:
    def __init__(self, rates: List[pymodels.Rate],
                index=None, qlcalendar=None):
        self.__rates = rates
        #self.__setting = setting
        #self.__current_date = current_date
        if index:
            self.__index = index

        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()    
    

    def helpers(self):
        ois_helpers = []
        for rate in self.__rates:
            ois_helper = ql.OISRateHelper(2, 
                                        ql.Period(rate.tenor),
                                        ql.QuoteHandle(ql.SimpleQuote(rate.rate/100)), 
                                        self.__index)
            ois_helpers.append(ois_helper)
        return ois_helpers


class IRS:
    def __init__(self, rates: List[pymodels.Rate], setting: pymodels.BondSetting,
                index=None, qlcalendar=None):
        self.__rates = rates
        self.__setting = setting
        #self.__current_date = current_date
        if index:
            self.__index = index

        if qlcalendar:
            self.__qlcalendar = qlcalendar
        else:
            self.__qlcalendar = ql.NullCalendar()    
    

    def helpers(self):
        irs_helpers = []
        frequency = qlc.ql_frequency[self.__setting.frequency]
        business_day = qlc.ql_business_day[self.__setting.business_day]
        day_count = qlc.ql_day_count[self.__setting.day_count]
        for rate in self.__rates:
            irs_helper = ql.SwapRateHelper(rate.rate/100, 
                                            ql.Period(rate.tenor), 
                                            self.__qlcalendar, 
                                            frequency, 
                                            business_day, 
                                            day_count, 
                                            self.__index)
            irs_helpers.append(irs_helper)
        return irs_helpers



class Curve:
    def __init__(self, day_count: qle.DayCount, deposits: Deposits = None, 
                parbond: ParBond = None, fra: FRAs = None, 
                ois: OIS=None, irs: IRS=None, qlcalendar=None):
        self.__day_count = day_count
        self.__deposits = deposits
        self.__parbond = parbond
        self.__fra = fra
        self.__ois = ois
        self.__irs = irs
        #self.__current_date = current_date
        #if qlcalendar:
        #    self.__qlcalendar = qlcalendar
        #else:
        #    self.__qlcalendar = ql.NullCalendar()  


    def piecewise(self, date: dt64 = None, method: qle.PiecewiseMethods = qle.PiecewiseMethods.logcubicdiscount):
        if date:
            vdate = ql.Date(datestr(date), '%Y-%m-%d')
        else:
            vdate = ql.Settings.instance().evaluationDate
        
        helpers = self.__deposits.helpers()
        helpers += self.__parbond.helpers()
        
        if self.__fra:
            helpers += self.__fra.helpers()
        if self.__ois:
            helpers += self.__ois.helpers()
        if self.__irs:
            helpers += self.__irs.helpers()

        day_count = qlc.ql_day_count[self.__day_count]

        if method == qle.PiecewiseMethods.loglineardiscount:
            t_structure = ql.PiecewiseLogLinearDiscount(vdate,
                                                    helpers,
                                                    day_count)
        elif method == qle.PiecewiseMethods.linearforward:
            t_structure = ql.PiecewiseLinearForward(vdate,
                                                    helpers,
                                                    day_count)
        elif method == qle.PiecewiseMethods.linearzero:
            t_structure = ql.PiecewiseLinearZero(vdate,
                                                helpers,
                                                day_count)
        elif method == qle.PiecewiseMethods.cubiczero:
            t_structure = ql.PiecewiseCubicZero(vdate,
                                                helpers,
                                                day_count)
        elif method == qle.PiecewiseMethods.splinecubicdiscount:
            t_structure = ql.PiecewiseSplineCubicDiscount(vdate,
                                                    helpers,
                                                    day_count)
        else:
            t_structure = ql.PiecewiseLogCubicDiscount(vdate,
                                                    helpers,
                                                    day_count)
        #return the term structure
        return t_structure
