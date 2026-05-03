import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def simulate_risk_management(file_path, stop_gain=400, stop_loss=-100, max_seq_loss=4):
    if not os.path.exists(file_path):
        print(f"Erro: {file_path} não encontrado.")
        return

    # 1. Carregar e preparar dados
    df = pd.read_csv(file_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M')
    df['Date'] = df['Time'].dt.date
    df = df.sort_values(by='Time')

    # 2. Simulação Dia a Dia
    results = []
    
    for date, day_trades in df.groupby('Date'):
        day_pnl = 0
        day_trades_executed = 0
        consecutive_losses = 0
        day_active = True
        
        for _, trade in day_trades.iterrows():
            if not day_active:
                continue
            
            # Executa o trade
            day_pnl += trade['Result_BRL']
            day_trades_executed += 1
            
            # Atualiza sequência de perdas
            if trade['Result_BRL'] < 0:
                consecutive_losses += 1
            else:
                consecutive_losses = 0
                
            # Verifica travas de segurança
            if day_pnl >= stop_gain:
                day_active = False # Stop Gain atingido
            elif day_pnl <= stop_loss:
                day_active = False # Stop Loss atingido
            elif consecutive_losses >= max_seq_loss:
                day_active = False # Sequência máxima de perdas
            
            results.append({
                'Time': trade['Time'],
                'Result_BRL': trade['Result_BRL'],
                'Daily_Stop_Active': not day_active,
                'Cumulative_PNL': day_pnl
            })

    # 3. Comparação de Resultados
    sim_df = pd.DataFrame(results)
    
    # Original (sem travas diárias)
    df['Equity_Original'] = df['Result_BRL'].cumsum()
    
    # Simulado (com as suas travas)
    # Importante: No simulado, trades após a trava ser atingida no dia são ignorados
    # mas o Result_BRL no DataFrame sim_df já reflete apenas os trades autorizados
    sim_df['Equity_Simulated'] = sim_df['Result_BRL'].cumsum()
    
    print(f"=== SIMULAÇÃO DE GERENCIAMENTO DE RISCO (5 ANOS) ===")
    print(f"Regras: Gain R$ {stop_gain} | Loss R$ {abs(stop_loss)} | Max Seq Loss: {max_seq_loss}")
    print("-" * 50)
    print(f"Resultado Original: R$ {df['Result_BRL'].sum():.2f}")
    print(f"Resultado Simulado: R$ {sim_df['Result_BRL'].sum():.2f}")
    
    # Cálculos de Drawdown
    def calc_drawdown(equity_series):
        peaks = equity_series.cummax()
        drawdown = (equity_series - peaks)
        return drawdown.min()

    dd_orig = calc_drawdown(df['Equity_Original'])
    dd_sim = calc_drawdown(sim_df['Equity_Simulated'])
    
    print(f"Drawdown Original: R$ {dd_orig:.2f}")
    print(f"Drawdown Simulado: R$ {dd_sim:.2f}")
    
    # 4. Gráfico Comparativo
    plt.figure(figsize=(15, 8))
    plt.plot(df['Time'], df['Equity_Original'], label='Raw Setup (Sem Travas)', color='gray', alpha=0.5)
    plt.plot(sim_df['Time'], sim_df['Equity_Simulated'], label='Gerenciamento Proposto (400/100/4L)', color='red', lw=2)
    plt.title('Impacto do Gerenciamento de Risco Diário (5 Anos)')
    plt.ylabel('Capital Acumulado (R$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('simulacao_gerenciamento_risco.png')
    
    print("\nGráfico salvo em 'simulacao_gerenciamento_risco.png'")

if __name__ == "__main__":
    simulate_risk_management("dna5y.csv", stop_gain=400, stop_loss=-100, max_seq_loss=4)
