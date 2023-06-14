from ctypes import *

from database import Hdf5Client

from utils import resample_timeframe, STRAT_PARAMS, get_library
import strategies.obv
  

def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):

    params_des = STRAT_PARAMS[strategy]

    params = dict()

    for p_code, p in params_des.items():
        while True:
            try:
                params[p_code] = p["type"](input(p["name"] + ": "))
                break
            except ValueError:
                continue

    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl, max_drawdown = strategies.obv.backtest(data, ma_period=params["ma_period"])

        return pnl, max_drawdown
 
    elif strategy == "psar":

        lib = get_library()

        obj = lib.Psar_new(exchange.encode(), symbol.encode(), tf.encode(), from_time, to_time)
        lib.Psar_execute_backtest(obj, params["initial_acc"], params["acc_increment"], params["max_acc"])
        pnl = lib.Psar_get_pnl(obj)
        max_drawdown = lib.Psar_get_max_dd(obj)

        return pnl, max_drawdown









