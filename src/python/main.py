
from line_flows_and_losses import calculate_method_comparison
from gauss_seidel import gauss_seidel
from newton_raphson import run_load_flow
from system_data import bus_data, gen_data

import pandas as pd
resultg,iterg,errg = gauss_seidel()
print("Gauss seidel converged in ",iterg, " iterations \n mismatch: ",errg)

resultn,itern,errn = run_load_flow()
print("Newton raphson converged in ",itern," iterations \n mismatch: ",errn)


comparison = calculate_method_comparison()

print("Voltage comparison: GS vs NR")
print("----------------------------")

gs = comparison["voltage"]["gs"][["Bus", "V_mag_pu", "V_ang_deg"]].rename(
    columns={"V_mag_pu": "GS_V_mag", "V_ang_deg": "GS_V_ang"}
)
nr = comparison["voltage"]["nr"][["Bus", "V_mag", "V_ang_deg"]].rename(
    columns={"V_mag": "NR_V_mag", "V_ang_deg": "NR_V_ang"}
)

vdf = gs.merge(nr, on="Bus")
print(vdf)

print("\nCurrent comparison: GS vs NR")
print("----------------------------")

gsc = comparison["current"]["gs"][["Bus", "I_pu"]].rename(
    columns={"I_pu": "GS_I_pu"}
)
nrc = comparison["current"]["nr"][["Bus", "I_pu"]].rename(
    columns={"I_pu": "NR_I_pu"}
)
cdf = gsc.merge(nrc, on="Bus")
print(cdf)

print("\nSending-end P/Q comparison: GS vs NR")
print("--------------------------------------")

gs_flow = comparison["line_flow"]["gs"][['from', 'to', 'P_from_MW', 'Q_from_MVAr']].rename(
    columns={
        'from': 'GS_from',
        'to': 'GS_to',
        'P_from_MW': 'GS_P_from_MW',
        'Q_from_MVAr': 'GS_Q_from_MVAr',
    }
)
nr_flow = comparison["line_flow"]["nr"][['from', 'to', 'P_from_MW', 'Q_from_MVAr']].rename(
    columns={
        'P_from_MW': 'NR_P_from_MW',
        'Q_from_MVAr': 'NR_Q_from_MVAr',
    }
)
flow_df = gs_flow.merge(
    nr_flow,
    how='outer',
    left_on=['GS_from', 'GS_to'],
    right_on=['from', 'to'],
)
flow_df = flow_df.drop(columns=['from', 'to'])
print(flow_df)

print("\nReceiving-end P/Q comparison: GS vs NR")
print("---------------------------------------")

gs_flow_to = comparison["line_flow"]["gs"][['from', 'to', 'P_to_MW', 'Q_to_MVAr']].rename(
    columns={
        'from': 'GS_from',
        'to': 'GS_to',
        'P_to_MW': 'GS_P_to_MW',
        'Q_to_MVAr': 'GS_Q_to_MVAr',
    }
)
nr_flow_to = comparison["line_flow"]["nr"][['from', 'to', 'P_to_MW', 'Q_to_MVAr']].rename(
    columns={
        'P_to_MW': 'NR_P_to_MW',
        'Q_to_MVAr': 'NR_Q_to_MVAr',
    }
)
flow_to_df = gs_flow_to.merge(
    nr_flow_to,
    how='outer',
    left_on=['GS_from', 'GS_to'],
    right_on=['from', 'to'],
)
flow_to_df = flow_to_df.drop(columns=['from', 'to'])
print(flow_to_df)

print("\nLoss comparison: GS vs NR")
print("--------------------------")

gs_loss = comparison["line_loss"]["gs"][['from', 'to', 'P_loss_MW', 'Q_loss_MVAr']].rename(
    columns={
        'from': 'GS_from',
        'to': 'GS_to',
        'P_loss_MW': 'GS_P_loss_MW',
        'Q_loss_MVAr': 'GS_Q_loss_MVAr',
    }
)
nr_loss = comparison["line_loss"]["nr"][['from', 'to', 'P_loss_MW', 'Q_loss_MVAr']].rename(
    columns={
        'P_loss_MW': 'NR_P_loss_MW',
        'Q_loss_MVAr': 'NR_Q_loss_MVAr',
    }
)
loss_df = gs_loss.merge(
    nr_loss,
    how='outer',
    left_on=['GS_from', 'GS_to'],
    right_on=['from', 'to'],
)
loss_df = loss_df.drop(columns=['from', 'to'])
print(loss_df)

