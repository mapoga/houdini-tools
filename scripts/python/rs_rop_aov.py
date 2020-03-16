aov_primary = {
    'category': 'primary',
    'aovs': [
        {   
            'parms': {
                'RS_aovID': 'DIRECTLIGHTING_DIFFUSE',
                'RS_aovSuffix': 'diffuse',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'DIFFUSE_TINT',
                'RS_aovSuffix': 'diffuseFilter',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'GI',
                'RS_aovSuffix': 'gi',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'DIRECTLIGHTING_REFLECTIONS',
                'RS_aovSuffix': 'specular',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'INDIRECTLIGHTING_REFLECTIONS',
                'RS_aovSuffix': 'reflection',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'BEAUTY',
                'RS_aovSuffix': 'beauty_aux',
                'RS_aovLightAllGroups': 1,
            },
            'enabled': True
        },
    ],
    'enabled': True
}

aov_secondary = {
    'category': 'secondary',
    'aovs': [
        {   
            'parms': {
                'RS_aovID': 'INDIRECTLIGHTING_REFRACTIONS',
                'RS_aovSuffix': 'refraction',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'EMISSION',
                'RS_aovSuffix': 'emission',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'SSS',
                'RS_aovSuffix': 'sss',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'VOLUMELIGHTING',
                'RS_aovSuffix': 'volume',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'CAUSTICS',
                'RS_aovSuffix': 'caustics',
            },
            'enabled': False
        },
    ],
    'enabled': False
}

aov_technical = {
    'category': 'technical',
    'aovs': [
        {   
            'parms': {
                'RS_aovID': 'World',
                'RS_aovSuffix': 'P',
                'RS_aovWorldFilter': 'CENTERSAMPLE',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'Depth',
                'RS_aovSuffix': 'Z',
                'RS_aovDeepFilter': 'CENTERSAMPLE',
                'RS_aovDeepEnvRays': 1,
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'Depth',
                'RS_aovSuffix': 'Z2',
                'RS_aovDeepFilter': 'FULL',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'NORMALS',
                'RS_aovSuffix': 'N',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'CUSTOM',
                'RS_aovSuffix': 'N2',
                'RS_aovCustomShader': '../Custom_AOVs/N2',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'CUSTOM',
                'RS_aovSuffix': 'P_rest',
                'RS_aovCustomShader': '../Custom_AOVs/P_rest/',
            },
            'enabled': False
        },
    ],
    'enabled': True
}

aov_motion = {
    'category': 'motion vectors',
    'aovs': [
        {   
            'parms': {
                'RS_aovID': 'MotionVectors',
                'RS_aovSuffix': 'V',
                'RS_aovMotionRaw': 1,
                'RS_aovMotionClamp': 1,
                'RS_aovMotionFilter': 0,
            },
            'enabled': True
        },
    ],
    'enabled': True
}

aov_crypto = {
    'category': 'cryptomatte',
    'aovs': [
        {   
            'parms': {
                'RS_aovID': 'CRYPTOMATTE',
                'RS_aovSuffix': 'crypto_Node',
                'RS_aovCryptomatteType': 'RS_BLOCKSINKCRYPTOMATTETYPE_MESHID',
            },
            'enabled': False
        },
        {   
            'parms': {
                'RS_aovID': 'CRYPTOMATTE',
                'RS_aovSuffix': 'crypto_Material',
                'RS_aovCryptomatteType': 'RS_BLOCKSINKCRYPTOMATTETYPE_MATERIALID',
            },
            'enabled': True
        },
        {   
            'parms': {
                'RS_aovID': 'CRYPTOMATTE',
                'RS_aovSuffix': 'path',
                'RS_aovCryptomatteType': 'RS_BLOCKSINKCRYPTOMATTETYPE_MESHIDUSINGFROMTOARRAYS',
            },
            'enabled': False
        },
    ],
    'enabled': True
}