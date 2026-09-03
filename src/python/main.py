
import system_data as sd
from line_flows_and_losses import calculate_line_flows_and_losses
from gauss_seidel import gauss_seidel
from newton_raphson import run_load_flow

print("Voltages and currents: ")
print("Gauss-Seidel")
print("########################")
resultg,iterg,error = gauss_seidel()
print(resultg)
print("Newton-Raphson")
print("########################")
resultn,itern,error = run_load_flow()
print(resultn)


line_flows_gs, line_flows_nr,losses_gs,losses_nr = calculate_line_flows_and_losses()
print("Gauss-Seidel line flows and losses:")
print("########################")
print("Line flows: ")
print("--------------------------")
print(line_flows_gs)
print("Line losses: ")
print("--------------------------")
print(losses_gs)


print("\nNewton-Raphson line flows and losses:")
print("########################")
print("Line flows: ")
print("--------------------------")
print(line_flows_nr)
print("Line losses: ")
print("--------------------------")
print(losses_nr)