outputCommon = {
    'category': 'common',
    'parms': {
        'RS_outputFileNamePrefix': '`$HIP`/../rdr_out/`$OS`/`$HIPNAME`/`$OS`.`$F4`.exr',
        'RS_aovAutocrop': 1,
        'RS_aovMultipart': 1,
    },
    'enabled': True
}

motionBlur = {
    'category': 'motion blur',
    'parms': {
        'MotionBlurEnabled': 1,
        'MotionBlurDeformationEnabled': 1,
        'RS_mbPoints': 1,
        'MotionBlurShutterEfficiencyForTrapezoidal': 0,
    },
    'enabled': True
}

GI = {
    'category': 'gi',
    'parms': {
        'PrimaryGIEngine': 'RS_GIENGINE_BRUTE_FORCE',
        'SecondaryGIEngine': 'RS_GIENGINE_BRUTE_FORCE',
        'BruteForceGINumRays': 128,
    },
    'enabled': True
}

sampling = {
    'category': 'sampling',
    'quality': 
    [
        {
            'quality': 'speed',
            'parms': 
            {
                'UnifiedMinSamples': 16,
                'UnifiedMaxSamples': 128,
                'UnifiedAdaptiveErrorThreshold': 0.003,
            },
            'checked': True
        },
        {
            'quality': 'good',
            'parms':
            {
                'UnifiedMinSamples': 64,
                'UnifiedMaxSamples': 1024,
                'UnifiedAdaptiveErrorThreshold': 0.003,
            }
        },
        {
            'quality': 'final',
            'parms':
            {
                'UnifiedMinSamples': 128,
                'UnifiedMaxSamples': 2048,
                'UnifiedAdaptiveErrorThreshold': 0.001,
            }
        },

    ],
    'enabled': True
}
