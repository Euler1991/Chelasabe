import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import manhattan_distances

beers_dict = {'Bohemia Oscura': 'Boh_Osc',
              'Corona': 'Cor',
              'Dos Equis Ambar': 'Dos_Equ_Amb',
              'Dos Equis Laguer': 'Dos_Equ_Lag',
              'Indio': 'Ind',
              'Modelo Especial': 'Mod_Esp',
              'Negra Modelo': 'Neg_Mod',
              'Sol': 'Sol',
              'Tecate Light': 'Tec_Lig',
              'Victoria': 'Vic'}

lager_dict = {'Pilsner': 'Pil',
              #'Pale Lager': 'Pal_Lag',
              'Amber Lager': 'Amb_Lag',
              'Bock': 'Boc',
              'Dark Lager': 'Dar_Lag'}

ale_dict = {'Wheat Beer':'Whe_Bee',
            'Pale Ale': 'Pal_Ale',
            'Indian Pale Ale': 'Ind_Pal_Ale',
            'Strong Ale': 'Str_Ale',
            'Brown Ale': 'Bro_Ale',
            'Stout': 'Sto'}

answers_df = pd.read_csv('../Code/Datasets/UTP.csv')

answers_names_dict = {'Marca temporal': 'Date',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Barrilito]': 'Bar',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Bohemia Clara]': 'Boh_Cla',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Bohemia Oscura]': 'Boh_Osc',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Bud Light]': 'Bud_Lig',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Corona]': 'Cor',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Dos Equis Laguer]': 'Dos_Equ_Lag',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Dos Equis Ambar]': 'Dos_Equ_Amb',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Indio]': 'Ind',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [León]': 'Leo',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Modelo Especial]': 'Mod_Esp',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Montejo]': 'Mon',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Negra Modelo]': 'Neg_Mod',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Pacífico]': 'Pac',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Sol]': 'Sol',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Tecate Roja]': 'Tec_Roj',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Tecate Light]': 'Tec_Lig',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para las siguientes cervezas comerciales. Si para alguna cerveza no tienes una opinión, escoge SR. [Victoria]': 'Vic',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Pale Lager]': 'Pal_Lag',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Pilsner]': 'Pil',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Amber Lager]': 'Amb_Lag',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Bock]': 'Boc',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Dark Lager]': 'Dar_Lag',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Wheat Beer]': 'Whe_Bee',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Pale Ale]': 'Pal_Ale',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Indian Pale Ale]': 'Ind_Pal_Ale',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Strong Ale]': 'Str_Ale',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Brown Ale]': 'Bro_Ale',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Porter]': 'Por',
                      'Califica del 1 (no me gusta) al 5 (me encanta) tu preferencia para los siguientes estilos. Si para algún estilo no tienes una opinión, escoge SR [Stout]': 'Sto'}
answers_df.rename(columns=answers_names_dict,
                  inplace=True)

answers_df.replace('SR', np.nan, inplace=True)

styles_null = []
beers_null = []
for i in range(len(answers_df.index)):
    styles_null.append(answers_df.loc[i, list(lager_dict.values()) + list(ale_dict.values())].isnull().sum())
    beers_null.append(answers_df.loc[i, list(beers_dict.values())].isnull().sum())

answers_df['style_nulls'] = styles_null
answers_df['beer_nulls'] = beers_null

answers_df = answers_df[(answers_df.style_nulls <= 4) & (answers_df.beer_nulls <= 4)]
answers_df.reset_index(drop=True, inplace=True)

comercials = list(beers_dict.values())
answers_df = answers_df.fillna(answers_df.median())


def drunk_distances(form):
    d_na = manhattan_distances([form], answers_df[comercials])
    d_na = d_na.max() - d_na
    A = answers_df[list(lager_dict.values()) + list(ale_dict.values())].to_numpy()
    A = A.astype(float)
    S_rec = np.dot(d_na, A)
    S_rec = S_rec / np.sum(d_na)
    return S_rec


def drink_team_rec(form):
    d_na = manhattan_distances([form], answers_df[comercials])
    top3 = list(d_na.argsort()[0][:5])
    drink_team = answers_df.loc[top3, list(lager_dict.values()) + list(ale_dict.values())].to_numpy().astype(float)
    rec = np.average(drink_team, axis=0)
    return rec
