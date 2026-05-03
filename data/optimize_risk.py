import pandas as pd
import numpy as np
import os
from tqdm import tqdm

def optimize_risk_grid(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: {file_path} não encontrado.")
        return

    # 1. Carregar dados
    df = pd.read_csv(file_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M')
    df['Date'] = df['Time'].dt.date
    df = df.sort_values(by='Time')

    # 2. Definir intervalos de busca
    losses_to_test = range(-50, -350, -25)     # Stop Loss Diário
    gains_to_test = range(200, 1050, 50)       # Stop Gain Diário
    seq_to_test = range(2, 7)                  # Sequência Máxima de Perdas
    
    results = []

    # Agrupar por data uma única vez para acelerar
    grouped = list(df.groupby('Date'))

    print("Iniciando Otimização em Grade (Grid Search)...")
    
    for sl in tqdm(losses_to_test):
        for sg in gains_to_test:
            for max_seq in seq_to_test:
                
                total_pnl = 0
                max_drawdown = 0
                equity = 0
                peak = 0
                trades_count = 0
                
                for date, day_trades in grouped:
                    day_pnl = 0
                    day_seq_loss = 0
                    day_active = True
                    
                    for _, trade in day_trades.iterrows():
                        if not day_active:
                            continue
                        
                        pnl = trade['Result_BRL']
                        day_pnl += pnl
                        equity += pnl
                        trades_count += 1
                        
                        # Atualiza drawdown
                        if equity > peak: peak = equity
                        dd = equity - peak
                        if dd < max_drawdown: max_drawdown = dd
                        
                        # Seq Loss
                        if pnl < 0: day_seq_loss += 1
                        else: day_seq_loss = 0
                        
                        # Travas
                        if day_pnl >= sg or day_pnl <= sl or day_seq_loss >= max_seq:
                            day_active = False
                    
                    total_pnl += day_pnl

                recovery_factor = total_pnl / abs(max_drawdown) if max_drawdown != 0 else 0
                
                results.append({
                    'Stop_Loss': sl,
                    'Stop_Gain': sg,
                    'Max_Seq': max_seq,
                    'Total_PNL': total_pnl,
                    'Max_DD': max_drawdown,
                    'Rec_Factor': recovery_factor,
                    'Trades': trades_count
                })

    # 3. Analisar Resultados
    results_df = pd.DataFrame(results)
    
    # Ordenar pelo Fator de Recuperação (Melhor Risco/Retorno)
    best_by_rf = results_df.sort_values(by='Rec_Factor', ascending=False).iloc[0]
    best_by_pnl = results_df.sort_values(by='Total_PNL', ascending=False).iloc[0]

    print("\n" + "="*50)
    print("MELHOR COMBINACAO (EFICIENCIA - FATOR REC.)")
    print(f"Stop Loss: R$ {best_by_rf['Stop_Loss']}")
    print(f"Stop Gain: R$ {best_by_rf['Stop_Gain']}")
    print(f"Max Seq Loss: {best_by_rf['Max_Seq']}")
    print(f"Lucro Total: R$ {best_by_rf['Total_PNL']:.2f}")
    print(f"Drawdown Max: R$ {best_by_rf['Max_DD']:.2f}")
    print(f"Fator Recuperacao: {best_by_rf['Rec_Factor']:.2f}")
    print("="*50)

    print("\n" + "="*50)
    print("MELHOR COMBINACAO (LUCRO BRUTO)")
    print(f"Stop Loss: R$ {best_by_pnl['Stop_Loss']}")
    print(f"Stop Gain: R$ {best_by_pnl['Stop_Gain']}")
    print(f"Max Seq Loss: {best_by_pnl['Max_Seq']}")
    print(f"Lucro Total: R$ {best_by_pnl['Total_PNL']:.2f}")
    print(f"Fator Recuperacao: {best_by_pnl['Rec_Factor']:.2f}")
    print("="*50)
    
    results_df.to_csv('otimizacao_risco_detalhada.csv', index=False)

if __name__ == "__main__":
    optimize_risk_grid("dna5y.csv")
