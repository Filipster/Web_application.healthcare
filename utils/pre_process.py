import pandas as pd
import numpy as np
import streamlit as st
import unidecode

class DataProcess:
    def __init__(self, df):
        self.df = df

    def excel_process(self):
        """Main process to excel files."""
        
        try:
            # Drop columns
            reduced_df = self.__drop_known_useless_columns(self.df)

            adjusted_text_df = self.__correct_text_errors(reduced_df)

        except Exception as e:
            # st.exception('Arquivo não corresponde ao layout PRAS.')
            st.exception(e)
        
        return adjusted_text_df

    def __drop_known_useless_columns(self, df):
        full_df = df.copy()
        mapped_cols = ['ENT_ID', 'ENT_RUC', 'ENT_SIM_TIP_EST', 'ENT_COD_PROV', 
               'ENT_DES_PROV', 'ENT_COD_CANT', 'ENT_COD_PARR', 'ENT_INT',
               'ENT_COD_ZON', 'ENT_DES_ZON', 'ENT_COD_DIS', 'ENT_DIST_DIS',
               'ENT_COD_CIR', 'ENT_COD_CIR', 'PROF_NOMBRECOMPLETO', 'PROF_APELLIDOS',
               'PROF_TIP_IDEN', 'PROF_IDEN', 'PROF_REG_NRO', 'PROF_CORREO',
               'PCTE_NOM', 'PCTE_APELLIDOS', 'PCTE_TIP_IDEN', 'PCTE_IDE',
               'PCTE_ANIOS', 'PCTE_MESES', 'PCTE_DIAS', 'PCTE_EDAD_COMPUESTA',
               'PCTE_ANIOS_EN_MESES', 'PCTE_IDE_REP', 'PCTE_TEL_CEL', 'PCTE_TEL_CON',
               'PCTE_TIP_BON', 'PCTE_COD_PROV', 'PCTE_DES_PROV', 'PCTE_COD_CANT',
               'PCTE_PARR', 'PCTE_DIR_CALL_PRI', 'PCTE_DIR_CALL_SEC', 'PCTE_DIR_REF',
               'PCTE_DIR_BARR', 'ATEMED_FECHAHORA_INICIO', 'ATEMED_FEC_FIN',
               'ATEMED_FECHAHORA_FIN', 'ATEMED_ID', 'ATEMED_EST',
               'FECHA_CARGA', 'ATEMED_SEG_PCTE', 'PCTE_DISC', 'PCTE_TIP_DISC',
               'PCTE_POR_DISC', 'Unnamed: 114', 'Unnamed: 115', 'Unnamed: 116',
               'Unnamed: 117', 'Unnamed: 118']
        
        cleaned_df = full_df.drop(mapped_cols, axis=1)
        return cleaned_df

    def __correct_text_errors(self, df):
        _df = df.copy()

        # Correcting Health Centers
        _rule = (_df.ENT_DES_TIP_EST.isna()) & (_df.ENT_NOM == 'CENTRO DE SALUD ZAMORA')
        _df.loc[_rule, 'ENT_DES_TIP_EST'] = 'CENTRO DE SALUD TIPO A'

        # Filling Professional Gender
        _df['PROF_SEXO'].rename({'NA': 'No info'}, inplace=True, axis=0)
        _df.loc[_df.PROF_SEXO.isna(), 'PROF_SEXO'] = 'No info'
        _df.loc[_df.PROF_SEXO == ' ', 'PROF_SEXO'] = 'No info'

        # Correcting Professional speciality
        _df['PROF_ESP_ATE'] = _df.PROF_ESP_ATE.apply(self.__remove_accents)
        _df.loc[_df.PROF_ESP_ATE == 'Medicina General Integral', 'PROF_ESP_ATE'] = 'Medicina General'
        _df.loc[_df.PROF_ESP_ATE == 'Psicologia Clinica ', 'PROF_ESP_ATE'] = 'Psicologia Clinica'
        _df.loc[_df.PROF_ESP_ATE == 'Medicina Del Trabajo, Medicina Ocupacional', 'PROF_ESP_ATE'] = 'Medicina Del Trabajo'
        _df.loc[_df.PROF_ESP_ATE == 'Medicina Del Trabajo, Medicina', 'PROF_ESP_ATE'] = 'Medicina Del Trabajo'

        # Correcting Sexual Orientation
        _ = ['NA', 'No sabe/No responde', np.isnan]
        _df.loc[_df.PCTE_ORI_SEX.isin(_), 'PCTE_ORI_SEX'] = 'No info'
        _ = ['Heterosexual', 'No info']
        _df.loc[~_df.PCTE_ORI_SEX.isin(_), 'PCTE_ORI_SEX'] = 'Homossexual'

        # Correcting Gender Id
        _ = ['Ninguno', 'No sabe/No responde', np.isnan]
        _df.loc[_df.PCTE_IDE_GEN.isin(_), 'PCTE_IDE_GEN'] = 'No info'

        # Correcting Nationality
        _df['PCTE_NACIONALIDAD'] = _df.PCTE_NACIONALIDAD.apply(self.__adj_etnics)
        _ = ['ESPAÑOL', 'ESPA?OL']
        _df.loc[_df.PCTE_NACIONALIDAD.isin(_), 'PCTE_NACIONALIDAD'] = 'ESPANOL'
        _ = ['ECUATOGUINEANO', 'ECUATOGUINEAN']
        _df.loc[_df.PCTE_NACIONALIDAD.isin(_), 'PCTE_NACIONALIDAD'] = 'ECUATOGUINEANO'

        # Correcting Ethnics and Tribe
        _df['PCTE_AUTID_ETN'] = _df.PCTE_AUTID_ETN.apply(self.__adj_etnics)
        _ = ['No Aplica', 'No sabe', 'Otro', np.isnan]
        _df.loc[_df.PCTE_AUTID_ETN.isin(_), 'PCTE_AUTID_ETN'] = 'No info'

        _ = ['No sabemos/No responde', np.isnan]
        _df.loc[_df.PCTE_NAC_ETN.isin(_), 'PCTE_NAC_ETN'] = 'No info'

        _ = ['No sabemos/No responde', np.isnan]
        _df.loc[_df.PCTE_PUEBLO.isin(_), 'PCTE_PUEBLO'] = 'No info'

        # Correcting Life Assurance
        _df['PCTE_SEG'] = _df.PCTE_SEG.apply(self.__remove_accents)
        _df['PCTE_SEG'] = _df['PCTE_SEG'].str.replace("?", "n")

        # Correcting Risk Group
        _df['PCTE_GRP_PRI'] = _df.PCTE_GRP_PRI.apply(self.__remove_accents)
        _df['PCTE_GRP_PRI_Embarazadas'] = _df.PCTE_GRP_PRI.str.contains('Embarazada')
        _df['PCTE_GRP_PRI_Discapacidad'] = _df.PCTE_GRP_PRI.str.contains('Discapacidad')
        _df['PCTE_GRP_PRI_Assedio_Sexual_Trabajo'] = _df.PCTE_GRP_PRI.str.contains('A Sexual')
        _df['PCTE_GRP_PRI_Violencia_Psicologica'] = _df.PCTE_GRP_PRI.str.contains('Violencia P')
        _df['PCTE_GRP_PRI_Violencia_Sexual'] = _df.PCTE_GRP_PRI.str.contains('Violencia S')
        _df['PCTE_GRP_PRI_Violencia_Fisica'] = _df.PCTE_GRP_PRI.str.contains('Violencia F')
        _df['PCTE_GRP_PRI_Maltrato_Infantil'] = _df.PCTE_GRP_PRI.str.contains('Maltrato')
        _df['PCTE_GRP_PRI_Enfermidades_Catastroficas'] = _df.PCTE_GRP_PRI.str.contains('Catastrof')
        _df['PCTE_GRP_PRI_Desastres_Naturales'] = _df.PCTE_GRP_PRI.str.contains('Desastres N')
        _df['PCTE_GRP_PRI_Desastres_Antropogenicos'] = _df.PCTE_GRP_PRI.str.contains('Antropo')
        _df['PCTE_GRP_PRI_Penitenciarios'] = _df.PCTE_GRP_PRI.str.contains('Privados')

        _ = ['PCTE_GRP_PRI_Embarazadas', 'PCTE_GRP_PRI_Discapacidad', 'PCTE_GRP_PRI_Assedio_Sexual_Trabajo',
            'PCTE_GRP_PRI_Violencia_Psicologica', 'PCTE_GRP_PRI_Violencia_Sexual', 'PCTE_GRP_PRI_Violencia_Fisica',
            'PCTE_GRP_PRI_Maltrato_Infantil', 'PCTE_GRP_PRI_Enfermidades_Catastroficas', 'PCTE_GRP_PRI_Desastres_Naturales',
            'PCTE_GRP_PRI_Desastres_Antropogenicos', 'PCTE_GRP_PRI_Penitenciarios']
        _df['PCTE_GRP_PRI_QTD'] = _df[_].sum(axis=1)
        _df.drop(['PCTE_GRP_PRI'], axis=1, inplace=True)
        _df[_] = _df[_].fillna(0)
        _df = _df.fillna('No info')

        return _df


    def __remove_accents(self, x):
        try:
            return unidecode.unidecode(x)
        except:
            return x

    def __adj_etnics(self, x):
        _ = str(x).split('/')
        return _[0]