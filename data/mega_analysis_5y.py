import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Configurações de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [16, 12]

def run_mega_analysis(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: {file_path} não encontrado.")
        return

    # 1. Carregar dados
    df = pd.read_csv(file_path, sep=';', encoding='latin1')
    df.columns = df.columns.str.strip()
    
    # Converter datas e extrair tempo
    df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M')
    df = df.sort_values(by='Time')
    df['Year'] = df['Time'].dt.year
    
    print(f"=== ANÁLISE GLOBAL DE 5 ANOS ({df['Year'].min()} - {df['Year'].max()}) ===")
    print(f"Total de Trades: {len(df)}")
    print(f"Lucro Bruto Total: R$ {df['Result_BRL'].sum():.2f}")
    print(f"Taxa de Acerto Geral: {(df['Result_BRL'] > 0).mean()*100:.2f}%")
    print("-" * 50)

    # 2. Performance Anual
    yearly = df.groupby('Year')['Result_BRL'].agg(['count', 'sum', lambda x: (x > 0).mean()*100])
    yearly.columns = ['Trades', 'Lucro_Total', 'WinRate_%']
    print("\n--- PERFORMANCE POR ANO ---")
    print(yearly)

    # 3. ATR THRESHOLD SWEEP (Otimização Matemática)
    atr_results = []
    # Testar filtros de ATR de 200 a 700
    for threshold in range(200, 750, 25):
        filtered_df = df[df['ATR_Entry'] <= threshold]
        if len(filtered_df) == 0: continue
        
        net_profit = filtered_df['Result_BRL'].sum()
        win_rate = (filtered_df['Result_BRL'] > 0).mean() * 100
        profit_factor = filtered_df[filtered_df['Result_BRL']>0]['Result_BRL'].sum() / abs(filtered_df[filtered_df['Result_BRL']<0]['Result_BRL'].sum())
        
        atr_results.append({
            'Threshold': threshold,
            'Trades': len(filtered_df),
            'Net_Profit': net_profit,
            'Win_Rate': win_rate,
            'Profit_Factor': profit_factor,
            'Trades_Cut_%': (1 - len(filtered_df)/len(df)) * 100
        })
    
    atr_sweep = pd.DataFrame(atr_results)
    best_atr = atr_sweep.loc[atr_sweep['Net_Profit'].idxmax()]
    
    print("\n--- OTIMIZAÇÃO DE FILTRO ATR ---")
    print(f"Melhor Filtro Sugerido: ATR_Entry <= {best_atr['Threshold']}")
    print(f"Lucro com Filtro: R$ {best_atr['Net_Profit']:.2f}")
    print(f"Trades Eliminados: {best_atr['Trades_Cut_%']:.2f}%")

    # 4. Análise de Horários (Heatmap)
    hourly_stats = df.groupby(['Year', 'EntryHour'])['Result_BRL'].sum().unstack().fillna(0)
    
    # 5. Visualizações
    fig, axes = plt.subplots(3, 1)
    
    # Plot 1: Lucro por Threshold de ATR
    sns.lineplot(data=atr_sweep, x='Threshold', y='Net_Profit', marker='o', ax=axes[0], color='green')
    axes[0].set_title('Lucro Acumulado vs Limite de ATR (Onde parar de operar?)')
    axes[0].axvline(best_atr['Threshold'], color='red', linestyle='--', label=f'Ponto Ótimo: {best_atr["Threshold"]}')
    axes[0].legend()
    
    # Plot 2: Heatmap de Horários por Ano
    sns.heatmap(hourly_stats, cmap='RdYlGn', center=0, annot=True, fmt='.0f', ax=axes[1])
    axes[1].set_title('Heatmap de Lucro/Prejuízo por Hora e Ano')
    
    # Plot 3: Equity Curve Comparativa
    df['Equity_NoFilter'] = df['Result_BRL'].cumsum()
    df_filtered = df[df['ATR_Entry'] <= best_atr['Threshold']].copy()
    df_filtered['Equity_Filtered'] = df_filtered['Result_BRL'].cumsum()
    
    axes[2].plot(df['Time'], df['Equity_NoFilter'], label='Sem Filtros', color='gray', alpha=0.6)
    axes[2].plot(df_filtered['Time'], df_filtered['Equity_Filtered'], label=f'Com Filtro ATR <= {best_atr["Threshold"]}', color='blue', lw=2)
    axes[2].set_title('Impacto do Filtro ATR na Curva de Capital (5 Anos)')
    axes[2].legend()
    
    plt.tight_layout()
    plt.savefig('mega_otimizacao_5y.png')
    
    # Salvar resultados
    atr_sweep.to_csv('otimizacao_atr_sweep.csv', index=False)
    print("\nGráficos salvos em 'mega_otimizacao_5y.png'")
    print("Dados de sweep salvos em 'otimizacao_atr_sweep.csv'")

if __name__ == "__main__":
    run_mega_analysis("dna5y.csv")
