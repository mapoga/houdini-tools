import hou
from PySide2 import QtCore
from PySide2 import QtWidgets
import rs_rop_parms

def create_aov_mat(context='/out/'):
    context_node = hou.node(context)

    # matnet
    matnet_name = 'Custom_AOVs'
    matnet = hou.node('/'.join([context, matnet_name]))
    if matnet == None:
        matnet = context_node.createNode('matnet', matnet_name)

    # P_rest
    p_rest_name = 'P_rest'
    p_rest = matnet.node('/'.join([matnet.path(), p_rest_name]))
    if p_rest == None:
        p_rest = matnet.createNode('redshift_vopnet', p_rest_name)

        user_data = p_rest.createNode('redshift::RSUserDataVector', 'rest')
        user_data.parm('attribute').set('rest')
        store_color = p_rest.createNode('redshift::StoreColorToAOV', 'store')
        store_color.setInput(0, user_data)
        store_color.setInput(1, user_data)
        store_color.parm('aov_name0').set('P_rest')

        mat = p_rest.node('/'.join([p_rest.path(), 'redshift_material1']))
        if mat == None:
            mat = p_rest.createNode('redshift_material', 'redshift_material1')

        mat.setInput(0, store_color)

    p_rest.layoutChildren(p_rest.children())

    # N2
    N2_name = 'N2'
    N2 = matnet.node('/'.join([matnet.path(), N2_name]))
    if N2 == None:
        N2 = matnet.createNode('redshift_vopnet', N2_name)

        state = N2.createNode('redshift::State', 'state')
        store = N2.createNode('redshift::StoreColorToAOV', 'store')
        store.setInput(0, state)
        store.setInput(1, state)
        store.parm('aov_name0').set('N2')

        mat = N2.node('/'.join([N2.path(), 'redshift_material1']))
        if mat == None:
            mat = N2.createNode('redshift_material', 'redshift_material1')

        mat.setInput(0, store)

    N2.layoutChildren(N2.children())

    matnet.layoutChildren(matnet.children())


def setParms(n, args):
    for key, val in args.items():
        n.parm(key).set(val)

def RS_addAovs(n, *args):
    for aov in args:
        i = RS_aovExists(n, aov['RS_aovID'], aov['RS_aovSuffix'])
        if(i == 0):
            RS_aov_add(n)
            i = RS_aov_count(n)

        for key, val in aov.items():
            parm = key+'_'+str(i)
            n.parm(parm).set(val)

def RS_removeAovs(n, *args):
    for aov_group in args:
        for aov in aov_group:
            i = RS_aovExists(n, aov['RS_aovID'], aov['RS_aovSuffix'])
            if i != 0:
                n.parm('RS_aov').removeMultiParmInstance(i-1)

def RS_aovExists(n, aovID, aovSuffix):
    count = RS_aov_count(n)
    for i in range(1, count+1):
        if(n.parm('RS_aovID_'+str(i)).evalAsString() == aovID):
            if(n.parm('RS_aovSuffix_'+str(i)).evalAsString() == aovSuffix):
                return i
    return 0

def RS_aov_clear(n):
    n.parm('RS_aov').set(0)

def RS_aov_count(n):
    return n.parm('RS_aov').eval()

def RS_aov_add(n, i=1):
    count = RS_aov_count(n)
    n.parm('RS_aov').set(count+i)
    return RS_aov_count(n)

def RS_aov_remove(n, i=1):
    count = RS_aov_count(n)
    n.parm('RS_aov').set(max(count-i), 0)
    return RS_aov_count(n)

def RS_ROP_nodes():
    nodes = hou.selectedNodes()
    nodes = [n for n in nodes if n.type().name() == 'Redshift_ROP']
    return nodes

class RS_Settings(QtWidgets.QGroupBox):
    def __init__(self, *args):
        QtWidgets.QGroupBox.__init__(self)

        self.setTitle('Settings')
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Top buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_defaults = QtWidgets.QPushButton('defaults')
        btn_layout.addWidget(self.btn_defaults)
        self.btn_defaults.clicked.connect(self.defaults)

        self.btn_all = QtWidgets.QPushButton('all')
        btn_layout.addWidget(self.btn_all)
        self.btn_all.clicked.connect(self.all)

        self.btn_none = QtWidgets.QPushButton('none')
        btn_layout.addWidget(self.btn_none)
        self.btn_none.clicked.connect(self.none)
        btn_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        self.layout.addLayout(btn_layout)

        # singles
        self.parms = [rs_rop_parms.outputCommon, rs_rop_parms.motionBlur, rs_rop_parms.GI]
        for p in self.parms:
            checkBox = QtWidgets.QCheckBox(p['category'])
            checkBox.setChecked(p['enabled'])
            checkBox.data = p
            self.layout.addWidget(checkBox)

        # radio
        for p in [rs_rop_parms.sampling]:
            h_lay_grp = QtWidgets.QHBoxLayout()
            grp = QtWidgets.QGroupBox(p['category'])
            grp.setCheckable(True)
            grp.setChecked(p['enabled'])
            h_lay = QtWidgets.QHBoxLayout()
            grp.setLayout(h_lay)
            self.layout.addLayout(h_lay_grp)
            btn_grp = QtWidgets.QButtonGroup()
            btn_grp.setExclusive(True)
            grp.data = p
            h_lay_grp.addWidget(grp)

            for i in p['quality']:

                checkBox = QtWidgets.QRadioButton(i['quality'])
                checkBox.data = i
                btn_grp.addButton(checkBox)
                h_lay.addWidget(checkBox)
                try:
                    checkBox.setChecked(i['checked'])
                except:
                    pass
            h_lay_grp.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
            h_lay.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))

        bottom_btn_layout = QtWidgets.QHBoxLayout()
        bottom_btn_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        self.btn_apply = QtWidgets.QPushButton('ROP Apply')
        bottom_btn_layout.addWidget(self.btn_apply)
        self.btn_apply.clicked.connect(self.apply)
        self.layout.addLayout(bottom_btn_layout)

    def apply(self):
        nodes = RS_ROP_nodes()
        for single in self.children():
            if isinstance(single, QtWidgets.QCheckBox):
                if single.isChecked():
                    for n in nodes:
                        setParms(n, single.data['parms'])

            if isinstance(single, QtWidgets.QGroupBox):
                for sampling in single.children():
                    if isinstance(sampling, QtWidgets.QRadioButton):
                        if sampling.isChecked():
                            for n in nodes:
                                setParms(n, sampling.data['parms'])

    def defaults(self):
        for single in self.children():
            if isinstance(single, QtWidgets.QCheckBox):
                single.setChecked(single.data['enabled'])

            if isinstance(single, QtWidgets.QGroupBox):
                single.setChecked(single.data['enabled'])
                for sampling in single.children():
                    if isinstance(sampling, QtWidgets.QRadioButton):
                        try:
                            sampling.setChecked(sampling.data['checked'])
                        except:
                            sampling.setChecked(False)

    def all(self):
        for single in self.children():
            if isinstance(single, QtWidgets.QCheckBox):
                single.setChecked(True)

            if isinstance(single, QtWidgets.QGroupBox):
                single.setChecked(True)

    def none(self):
        for single in self.children():
            if isinstance(single, QtWidgets.QCheckBox):
                single.setChecked(False)

            if isinstance(single, QtWidgets.QGroupBox):
                single.setChecked(False)
                for sampling in single.children():
                    if isinstance(sampling, QtWidgets.QRadioButton):
                        sampling.setChecked(False)


class RS_AOV(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self)
        self.aov_categories = args

        self.setWindowTitle('RS AOV')
        layout = QtWidgets.QVBoxLayout()


        self.aovs = QtWidgets.QGroupBox('AOVs')
        aov_vert = QtWidgets.QVBoxLayout()
        self.aovs.setLayout(aov_vert)
        aovs_layout = QtWidgets.QHBoxLayout()

        # Top buttons
        aov_btn_layout = QtWidgets.QHBoxLayout()
        self.btn_defaults = QtWidgets.QPushButton('defaults')
        aov_btn_layout.addWidget(self.btn_defaults)
        self.btn_defaults.clicked.connect(self.defaults)

        self.btn_all = QtWidgets.QPushButton('all')
        aov_btn_layout.addWidget(self.btn_all)
        self.btn_all.clicked.connect(self.all)

        self.btn_none = QtWidgets.QPushButton('none')
        aov_btn_layout.addWidget(self.btn_none)
        self.btn_none.clicked.connect(self.none)
        aov_btn_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        aov_vert.addLayout(aov_btn_layout)

        # AOVs
        aov_vert.addLayout(aovs_layout)
        layout.addWidget(self.aovs)
        for c in self.aov_categories:
            aovs_layout.addWidget(self.create_category(c))

        # Bottom buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        self.btn_clear = QtWidgets.QPushButton('ROP Clear')
        btn_layout.addWidget(self.btn_clear)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_add = QtWidgets.QPushButton('ROP Add')
        btn_layout.addWidget(self.btn_add)
        self.btn_add.clicked.connect(self.add)

        self.btn_replace = QtWidgets.QPushButton('ROP Replace')
        btn_layout.addWidget(self.btn_replace)
        self.btn_replace.clicked.connect(self.replace)
        aov_vert.addLayout(btn_layout)

        self.setLayout(layout)

    def clear(self):

        for n in RS_ROP_nodes():
            RS_aov_clear(n)

    def add(self):
        nodes = RS_ROP_nodes()
        all_aovs = self.aovs
        ch = all_aovs.children()
        for cat in all_aovs.children():
            if isinstance(cat, QtWidgets.QGroupBox):
                if cat.isChecked():
                    for aov in cat.children():
                        if isinstance(aov, QtWidgets.QCheckBox):
                            if aov.isChecked():
                                for n in nodes:
                                    RS_addAovs(n, aov.data['parms'])
        create_aov_mat()


    def replace(self):
        self.clear()
        self.add()

    def defaults(self):
        all_aovs = self.aovs
        ch = all_aovs.children()
        for cat in all_aovs.children():
            if isinstance(cat, QtWidgets.QGroupBox):
                cat.setChecked(cat.data['enabled'])
                for aov in cat.children():
                    if isinstance(aov, QtWidgets.QCheckBox):
                        aov.setChecked(aov.data['enabled'])

    def all(self):
        all_aovs = self.aovs
        ch = all_aovs.children()
        for cat in all_aovs.children():
            if isinstance(cat, QtWidgets.QGroupBox):
                cat.setChecked(True)
                for aov in cat.children():
                    if isinstance(aov, QtWidgets.QCheckBox):
                        aov.setChecked(True)

    def none(self):
        all_aovs = self.aovs
        ch = all_aovs.children()
        for cat in all_aovs.children():
            if isinstance(cat, QtWidgets.QGroupBox):
                cat.setChecked(False)
                for aov in cat.children():
                    if isinstance(aov, QtWidgets.QCheckBox):
                        aov.setChecked(False)

    def create_category(self, cat):
        grp = QtWidgets.QGroupBox(cat['category'])
        grp.data = cat
        vertical = QtWidgets.QVBoxLayout()
        grp.setLayout(vertical)
        grp.setCheckable(True)

        for aov in cat['aovs']:
            checkBox = QtWidgets.QCheckBox(aov['parms']['RS_aovSuffix'])
            checkBox.setChecked(aov['enabled'])
            checkBox.data = aov
            vertical.addWidget(checkBox)
        vertical.addSpacerItem(QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grp.setChecked(cat['enabled'])
        return grp
