import requests
import pandas as pd

def get_world_bank_data(indicator_code, country='all', format_type='json', date_range='2010:2021'):
    """
    Fetch data from the World Bank v2 API for a given indicator code.
    """
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}?date={date_range}&format={format_type}&per_page=500"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur HTTP : Impossible de récupérer les données pour {indicator_code}. Statut {response.status_code}")
        return None
    
    try:
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            df = pd.json_normalize(data[1])
            df = df[['country.value', 'date', 'value']]
            df.columns = ['Country', 'Year', 'Value']
            return df
        else:
            print(f"Erreur de structure de données pour l'indicateur {indicator_code}: {data}")
            return None
    except ValueError:
        print(f"Erreur : La réponse de l'API pour {indicator_code} n'est pas en JSON valide.")
        return None

# List of comprehensive ESG indicators for v2 API
indicators = {
    # Environment Indicators
    'CO2 Emissions (kt)': 'EN.ATM.CO2E.KT',
    'CO2 Emissions (metric tons per capita)': 'EN.ATM.CO2E.PC',
    'CO2 Emissions per GDP (kg per PPP $)': 'EN.ATM.CO2E.PP.GD',
    'Methane Emissions (kt of CO2 equivalent)': 'EN.ATM.METH.KT.CE',
    'Nitrous Oxide Emissions (kt of CO2 equivalent)': 'EN.ATM.NOXE.KT.CE',
    'Greenhouse Gas Emissions (CO2 equivalent)': 'EN.ATM.GHGT.KT.CE',
    'Renewable Energy Consumption (% of total energy consumption)': 'EG.FEC.RNEW.ZS',
    'Forest Area (% of land area)': 'AG.LND.FRST.ZS',
    'Energy Use (kg of oil equivalent per capita)': 'EG.USE.PCAP.KG.OE',
    'Annual Change in Forest Area (%)': 'AG.LND.FRST.K2',
    'Electricity Access (% of population)': 'EG.ELC.ACCS.ZS',

    # Social Indicators
    'Access to Safe Water (% of population)': 'SH.H2O.BASW.ZS',
    'Life Expectancy at Birth': 'SP.DYN.LE00.IN',
    'Primary School Enrollment (% gross)': 'SE.PRM.ENRR',
    'Access to Health Services': 'SH.STA.BRTC.ZS',
    'Unemployment Rate (% of total labor force)': 'SL.UEM.TOTL.ZS',
    'Poverty Headcount Ratio (% of population below $1.90/day)': 'SI.POV.DDAY',
    'Youth Literacy Rate (% ages 15-24)': 'SE.ADT.1524.LT.ZS',
    'Female Labor Force Participation Rate (% of female population ages 15+)': 'SL.TLF.CACT.FE.ZS',

    # Governance Indicators
    'Control of Corruption (index)': 'CC.EST',
    'Government Effectiveness (index)': 'GE.EST',
    'Regulatory Quality (index)': 'RQ.EST',
    'Political Stability and Absence of Violence (index)': 'PV.EST',
    'Rule of Law (index)': 'RL.EST'
}

# Fetch data for each indicator using the v2 API
esg_data = {}
for name, code in indicators.items():
    print(f"Récupération des données pour l'indicateur : {name}")
    result = get_world_bank_data(code)
    esg_data[name] = result
    
    if result is not None:
        print(f"Données récupérées avec succès pour {name}. Aperçu :")
        print(result.head())
    else:
        print(f"Aucune donnée disponible pour l'indicateur : {name}")

# Summary of retrieved data
print("\nRésumé des indicateurs ESG récupérés :")
for name, df in esg_data.items():
    if df is not None:
        print(f"{name} - {len(df)} lignes récupérées")
    else:
        print(f"{name} - Aucune donnée")
